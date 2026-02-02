from openapi_server.database.utils_queries import validate_data, convert_str_to_array
from openapi_server.repositories.internship_repository import InternshipRepository

internship_repo = InternshipRepository()

def delete_internship(internship_id: str):
    return internship_repo.delete(internship_id)

def get_internship_by_id(internship_id: str):
    return internship_repo.get_by_id(internship_id)

def add_internship(internship):
    internship = validate_data(internship)
    return internship_repo.add(internship)

def get_internships(position=None,
                    department=None,
                    skills=None,
                    employment_type=None,
                    hours_min = None,
                    hours_max = None,
                    status=None,
                    offset: int = 0,
                    limit: int = 10,
                    sort_by="position",
                    sort_order="asc", ):
    employment_type = convert_str_to_array(employment_type)
    filters = {
        "department": department,
        "position": position,
        "skills": skills,
        "employment_type": employment_type,
        "hours_per_week": {"min": hours_min, "max": hours_max},
        "status": status,
    }
    return internship_repo.get_all(filters, limit=limit, offset=offset, sort_by=sort_by, sort_order=sort_order)


def update_internship(internship_id: str, new_values: dict):
    internship = validate_data(new_values)
    return internship_repo.update(internship_id, internship)

