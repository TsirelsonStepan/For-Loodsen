from typing import List

from openapi_server.config import VALID_EMPLOYMENT_TYPES


def convert_str_to_array(employment_type_str: str) -> List[str]:
    """Преобразует строку employmentType в массив."""
    if not employment_type_str:
        return []
    return [type.strip() for type in employment_type_str.split(',')]

def validate_employment_types(employment_types: List[str]) -> List[str]:
    """Проверка всех значений employmentType на соответствие enum и удаление дубликатов"""
    seen = set()
    result = []
    for et in employment_types:
        if et not in VALID_EMPLOYMENT_TYPES:
            raise ValueError(f"Invalid value for employment_type: {et}. Must be one of {VALID_EMPLOYMENT_TYPES}")
        if et not in seen:
            seen.add(et)
            result.append(et)
    return result

def validate_data(data: dict) -> dict:
    """Проверка данных кандидата и преобразование строковых значений в массивы"""
    if 'employment_type' in data:
        data['employment_type'] = convert_str_to_array(data['employment_type'])
        data['employment_type'] = validate_employment_types(data['employment_type'])

    if 'skills' in data:
        data['skills'] = convert_str_to_array(data['skills'])

    return data
