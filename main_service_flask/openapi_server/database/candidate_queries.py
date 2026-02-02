from openapi_server.database.utils_queries import validate_data, convert_str_to_array
from openapi_server.repositories.candidate_repository import CandidateRepository

candidate_repo = CandidateRepository()

def delete_candidate(candidate_id: str):
    return candidate_repo.delete(candidate_id)


def get_candidate_by_id(candidate_id: str):
    return candidate_repo.get_by_id(candidate_id)


def add_candidate(candidate):
    candidate = validate_data(candidate)
    return candidate_repo.add(candidate)


def get_candidates(name=None,
                   phone=None,
                   email=None,
                   skills=None,
                   position=None,
                   hours_min=None,
                   hours_max=None,
                   employment_type=None,
                   offset: int = 0,
                   limit: int = 10,
                   sort_by="name",
                   sort_order="asc", ):
    employment_type = convert_str_to_array(employment_type)
    filters = {
        "name": name,
        "email": email,
        "phone": phone,
        "position": position,
        "skills": skills,
        "hours_per_week": {"min": hours_min, "max": hours_max},
        "employment_type": employment_type,
    }
    return candidate_repo.get_all(filters, limit=limit, offset=offset, sort_by=sort_by, sort_order=sort_order)


def update_candidate(candidate_id: str, new_values: dict):
    candidate = validate_data(new_values)
    return candidate_repo.update(candidate_id, candidate)

def import_candidates(files):
    return candidate_repo.import_from_csv(files)

def export_candidates(name=None,
                   phone=None,
                   email=None,
                   skills=None,
                   position=None,
                   hours=None,
                   employment_type=None,
                   offset: int = 0,
                   limit: int = 10,
                   sort_by="name",
                   sort_order="asc", ):
    filters = {
        "name": name,
        "email": email,
        "phone": phone,
        "position": position,
        "skills": skills,
        "hours_per_week": hours,
        "employment_type": employment_type,
    }
    return candidate_repo.export_to_csv(filters, limit=limit, offset=offset, sort_by=sort_by, sort_order=sort_order)
