import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.add_internship200_response import AddInternship200Response  # noqa: E501
from openapi_server.models.get_internships200_response import GetInternships200Response  # noqa: E501
from openapi_server.models.internship import Internship  # noqa: E501
from openapi_server.models.internship_with_id import InternshipWithId  # noqa: E501
from openapi_server import util
import openapi_server.database.internship_queries as queries

def add_internship(body):  # noqa: E501
    """Добавить запрос на стажёра

     # noqa: E501

    :param body:
    :type body: dict | list[dict] | bytes

    :rtype: Union[InternshipWithId, Tuple[InternshipWithId, int], Tuple[InternshipWithId, int, Dict[str, str]]
    """
    data = body
    if connexion.request.is_json:
        data = connexion.request.get_json()

    if isinstance(data, list):
        internships = [Internship.from_dict(item) for item in data]
        internship_dict = [internship.to_dict() for internship in internships]
        new_internship = [queries.add_internship(internship) for internship in internship_dict]
        return new_internship, 201
    else:
        internship = Internship.from_dict(data)
        internship_dict = internship.to_dict()# noqa: E501
        new_internship =  queries.add_internship(internship_dict)
        return new_internship, 201


def delete_internship(internship_id):  # noqa: E501
    """Удалить запрос на стажёра

     # noqa: E501

    :param internship_id: 
    :type internship_id: str
    :type internship_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return queries.delete_internship(internship_id)


def get_internshipby_id(internship_id):  # noqa: E501
    """Получить стажировку по ID

     # noqa: E501

    :param internship_id: 
    :type internship_id: str
    :type internship_id: str

    :rtype: Union[InternshipWithId, Tuple[InternshipWithId, int], Tuple[InternshipWithId, int, Dict[str, str]]
    """
    return queries.get_internship_by_id(internship_id)


def get_internships(position=None, status = None, department=None, hours_min = None, hours_max = None, employment_type=None, skills = None, limit=None, offset=None, sort_by=None, sort_order=None):  # noqa: E501
    """Получить список всех стажировок

     # noqa: E501

    :param position: Фильтрация стажировок по должности
    :type position: str
    :param status:
    :type status: str
    :param skills:
    :type skills: str
    :param hours_min:
    :type hours_min: int
    :param hours_max:
    :type hours_max: int
    :param employment_type:
    :type employment_type: str
    :param department: Фильтрация стажировок по департаменту
    :type department: str
    :param limit: Количество стажировок на одной странице
    :type limit: int
    :param offset: Количество стажировок, которые следует пропустить перед возвращением результатов
    :type offset: int
    :param sort_by: Поле по которому сортировать
    :type sort_by: str
    :param sort_order: Порядок сортировки (asc - порядок возрастания для чисел, алфавитный порядок для строк, dsc - наоборот)
    :type sort_order: str

    :rtype: Union[GetInternships200Response, Tuple[GetInternships200Response, int], Tuple[GetInternships200Response, int, Dict[str, str]]
    """
    return queries.get_internships(position = position,
                                   department= department,
                                   skills = skills,
                                   hours_max=hours_max,
                                   hours_min=hours_min,
                                   status=status,
                                   employment_type = employment_type,
                                   limit=  limit,
                                   offset= offset,
                                   sort_by= sort_by,
                                   sort_order= sort_order,)


def update_internship(internship_id, body):  # noqa: E501
    """Обновить запрос на стажёра

     # noqa: E501

    :param internship_id: 
    :type internship_id: str
    :type internship_id: str
    :param internship: 
    :type internship: dict | bytes

    :rtype: Union[InternshipWithId, Tuple[InternshipWithId, int], Tuple[InternshipWithId, int, Dict[str, str]]
    """
    internship = body
    if connexion.request.is_json:
        internship = Internship.from_dict(connexion.request.get_json())  # noqa: E501
    internship_dict = internship.to_dict()
    updated_internship = queries.update_internship(internship_id, internship_dict)
    return updated_internship

