from typing import Dict, Type, Optional, Any
from sqlalchemy import func, or_
from sqlalchemy.orm import Query
from sqlalchemy.sql.schema import Table

from openapi_server.config import MODEL_CONFIG, CAMEL_TO_SNAKE
from openapi_server.database.init_database import Session
from openapi_server.database.tables import SkillDB, CandidateDB, candidate_skills, InternshipDB, internship_skills


def apply_sorting(query: Query, sort_by: str, sort_order: str) -> Query:
    """Применяет сортировку к SQLAlchemy запросу.

    Args:
        query: SQLAlchemy запрос для сортировки.
        sort_by: Поле для сортировки (может быть в camelCase или snake_case).
        sort_order: Порядок сортировки ("asc" или "dsc").

    Returns:
        Отсортированный SQLAlchemy запрос.

    Raises:
        ValueError: Если модель не поддерживается.
    """
    model = query.column_descriptions[0]["type"]
    config = MODEL_CONFIG.get(model.__name__)
    if not config:
        raise ValueError(f"Unsupported model: {model.__name__}")

    sort_by = CAMEL_TO_SNAKE.get(sort_by, sort_by)

    allowed_fields = {
        col.name: getattr(model, col.name) for col in model.__table__.columns
    }

    return _apply_sort(query, sort_by, sort_order, config, allowed_fields)


def _apply_sort(
        query: Query,
        sort_by: str,
        sort_order: str,
        config: Dict[str, Any],
        allowed_fields: Dict[str, Any],
) -> Query:
    """Применяет сортировку для конкретного поля."""
    if sort_by == "skills":
        return _apply_skills_sort(query, sort_order, config)

    sort_by = sort_by if sort_by in allowed_fields else "position"
    column = allowed_fields[sort_by]

    return query.order_by(column.desc() if sort_order == "dsc" else column.asc())


def _apply_skills_sort(query: Query, sort_order: str, config: Dict[str, Any]) -> Query:
    """Применяет сортировку по количеству скиллов."""
    model = config["model"]
    skills_table = config["skills_table"]
    skills_count = func.count(SkillDB.uuid).label("skills_count")

    return (
        query.outerjoin(skills_table, model.uuid == skills_table.c[f"{model.__name__.lower()}_uuid"])
        .outerjoin(SkillDB, skills_table.c.skill_uuid == SkillDB.uuid)
        .group_by(model.uuid)
        .order_by(skills_count.desc() if sort_order == "dsc" else skills_count.asc())
    )


def apply_filters(query: Query, filters: Dict[str, Any]) -> Query:
    """Применяет фильтры к SQLAlchemy запросу на основе предоставленных параметров.

    Args:
        query: SQLAlchemy запрос для фильтрации.
        filters: Словарь с фильтрами (ключ - поле, значение - значение фильтра).

    Returns:
        Отфильтрованный SQLAlchemy запрос.

    Raises:
        ValueError: Если модель не поддерживается.
    """
    if not filters:
        return query

    model = query.column_descriptions[0]["type"]
    config = MODEL_CONFIG.get(model.__name__)
    if not config:
        raise ValueError(f"Unsupported model: {model.__name__}")

    for field, value in filters.items():
        if value is None or value == "":
            continue
        query = _apply_field_filter(query, field, value, model, config)

    return query

def _apply_field_filter(
    query: Query,
    field: str,
    value: Any,
    model: Type,
    config: Dict[str, Any],
) -> Query:
    """Применяет фильтр для конкретного поля."""
    handlers = {
        "skills": lambda q, v: _apply_skills_filter(q, v, model, config["skills_table"], config["uuid_column"]),
        "employment_type": lambda q, v: _apply_employment_type_filter(q, v, config["model"]),
        "status": lambda q, v: _apply_status_filter(q, v, config["model"]),
    }

    if field in handlers:
        return handlers[field](query, value)
    if hasattr(model, field):
        return _apply_generic_filter(query, field, value, model)
    return query

def _apply_skills_filter(
    query: Query,
    value: Any,
    model: Type,
    skills_table: Table,
    uuid_column: Any,
) -> Query:
    """Применяет фильтр по скиллам."""
    if isinstance(value, list):
        clean_skills = [skill.strip().lower() for skill in value if skill.strip()]
        if clean_skills:
            subquery = (
                Session()
                .query(uuid_column)
                .join(SkillDB, skills_table.c.skill_uuid == SkillDB.uuid)
                .filter(func.lower(SkillDB.name).in_(clean_skills))
                .group_by(uuid_column)
                .having(func.count(SkillDB.uuid) == len(clean_skills))
            )
            return query.filter(model.uuid.in_(subquery))
    else:
        return (
            query.join(skills_table, model.uuid == uuid_column)
            .join(SkillDB, skills_table.c.skill_uuid == SkillDB.uuid)
            .filter(SkillDB.name.ilike(f"%{value}%"))
        )
    return query

def _apply_employment_type_filter(query: Query, value: Any, model: Type) -> Query:
    """Применяет фильтр по employment_type."""
    employment_values = value if isinstance(value, list) else [value.strip()]
    return query.filter(model.employment_type.contains(employment_values))

def _apply_status_filter(query: Query, value: Any, model: Type) -> Query:
    """Применяет фильтр по status для InternshipDB."""
    if model.__name__ != "InternshipDB":
        return query  # Игнорируем, если модель не InternshipDB
    values = value if isinstance(value, list) else [v.strip() for v in value.split(",") if v.strip()]
    if values:
        return query.filter(model.status.in_(values))
    return query

def _apply_generic_filter(query: Query, field: str, value: Any, model: Type) -> Query:
    """Применяет общий фильтр для полей модели."""
    column = getattr(model, field)

    if field == "hours_per_week" and isinstance(value, dict):
        min_hours = value.get("min")
        max_hours = value.get("max")
        if min_hours is not None:
            query = query.filter(column >= min_hours)
        if max_hours is not None:
            query = query.filter(column <= max_hours)
    elif isinstance(value, str) and value.strip():
        cleaned_value = value.strip().lower()
        query = query.filter(func.lower(column).ilike(f"%{cleaned_value}%"))
    elif isinstance(value, list) and value:
        cleaned_values = [v.strip().lower() for v in value if v.strip()]
        query = query.filter(or_(*[func.lower(column).ilike(f"%{v}%") for v in cleaned_values]))
    else:
        query = query.filter(column == value)

    return query