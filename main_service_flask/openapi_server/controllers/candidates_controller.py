import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.database.candidate_queries import candidate_repo
from openapi_server.models.candidate import Candidate  # noqa: E501
from openapi_server.models.candidate_with_id import CandidateWithId  # noqa: E501
from openapi_server.models.get_candidates200_response import GetCandidates200Response  # noqa: E501
from openapi_server.models.pagination import Pagination  # noqa: E501
from openapi_server import util

import openapi_server.database.candidate_queries as queries

def add_candidate(body):  # noqa: E501
    """Добавить кандидата в стажёры

     # noqa: E501

    :param candidate: 
    :type candidate: dict | bytes

    :rtype: Union[CandidateWithId, Tuple[CandidateWithId, int], Tuple[CandidateWithId, int, Dict[str, str]]
    """
    candidate = body
    if connexion.request.is_json:
        candidate = Candidate.from_dict(connexion.request.get_json())  # noqa: E501
    candidate_dict = candidate.to_dict()
    new_candidate = queries.add_candidate(candidate_dict)
    return new_candidate, 201

def delete_candidate(candidate_id):  # noqa: E501
    """Удалить кандидата в стажёры

     # noqa: E501

    :param candidate_id: 
    :type candidate_id: str
    :type candidate_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return queries.delete_candidate(candidate_id)


def export_candidates(candidate_name=None,
                      candidate_phone=None,
                      candidate_email=None,
                      candidate_skills=None,
                      candidate_position=None,
                      candidate_hours=None,
                      candidate_employment_type=None,
                      limit=None,
                      offset=None,
                      sort_by=None,
                      sort_order=None):  # noqa: E501
    """Экспортировать таблицу стажёров из базы данных в CSV файл

     # noqa: E501

    :param candidate_name: 
    :type candidate_name: str
    :param candidate_phone: 
    :type candidate_phone: str
    :param candidate_email: 
    :type candidate_email: str
    :param candidate_skills: 
    :type candidate_skills: List[str]
    :param candidate_position: 
    :type candidate_position: str
    :param candidate_hours: 
    :type candidate_hours: int
    :param candidate_employment_type: 
    :type candidate_employment_type: str
    :param limit: Количество кандидатов на одной странице
    :type limit: int
    :param offset: Количество кандидатов, которые следует пропустить перед возвращением результатов
    :type offset: int
    :param sort_by: Поле по которому сортировать
    :type sort_by: str
    :param sort_order: Порядок сортировки (asc - порядок возрастания для чисел, алфавитный порядок для строк, dsc - наоборот)
    :type sort_order: str

    :rtype: Union[file, Tuple[file, int], Tuple[file, int, Dict[str, str]]
    """
    return queries.export_candidates(name = candidate_name,
                                phone=candidate_phone,
                                email=candidate_email,
                                skills=candidate_skills,
                                position=candidate_position,
                                hours=candidate_hours,
                                employment_type=candidate_employment_type,
                                limit=limit,
                                offset=offset,
                                sort_by=sort_by,
                                sort_order=sort_order)


def get_candidateby_id(candidate_id):  # noqa: E501
    """Получить кандидата в стажеры по ID

     # noqa: E501

    :param candidate_id: 
    :type candidate_id: str
    :type candidate_id: str

    :rtype: Union[CandidateWithId, Tuple[CandidateWithId, int], Tuple[CandidateWithId, int, Dict[str, str]]
    """
    return queries.get_candidate_by_id(candidate_id)

def get_candidates(candidate_name=None,
                   candidate_phone=None,
                   candidate_email=None,
                   candidate_skills=None,
                   candidate_position=None,
                   candidate_hours_min=None,
                   candidate_hours_max=None,
                   candidate_employment_type=None,
                   limit=None,
                   offset=None,
                   sort_by=None,
                   sort_order=None):  # noqa: E501
    """Получить список всех кандидатов в стажёры

     # noqa: E501

    :param candidate_name: 
    :type candidate_name: str
    :param candidate_phone: 
    :type candidate_phone: str
    :param candidate_email: 
    :type candidate_email: str
    :param candidate_skills: 
    :type candidate_skills: List[str]
    :param candidate_position: 
    :type candidate_position: str
    :param candidate_hours_min:
    :type candidate_hours_min: int
    :param candidate_hours_max:
    :type candidate_hours_max: int
    :param candidate_employment_type: 
    :type candidate_employment_type: str
    :param limit: Количество кандидатов на одной странице
    :type limit: int
    :param offset: Количество кандидатов, которые следует пропустить перед возвращением результатов
    :type offset: int
    :param sort_by: Поле по которому сортировать
    :type sort_by: str
    :param sort_order: Порядок сортировки (asc - порядок возрастания для чисел, алфавитный порядок для строк, dsc - наоборот)
    :type sort_order: str

    :rtype: Union[GetCandidates200Response, Tuple[GetCandidates200Response, int], Tuple[GetCandidates200Response, int, Dict[str, str]]
    """
    return queries.get_candidates(name = candidate_name,
                                  phone=candidate_phone,
                                  email=candidate_email,
                                  skills=candidate_skills,
                                  position=candidate_position,
                                  hours_min=candidate_hours_min,
                                  hours_max=candidate_hours_max,
                                  employment_type=candidate_employment_type,
                                  limit=limit,
                                  offset=offset,
                                  sort_by=sort_by,
                                  sort_order=sort_order)


def import_candidates(file=None):  # noqa: E501
    """Импортировать в базу данных стажёров из CSV файла

     # noqa: E501

    :param file: CSV file
    :type file: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return queries.import_candidates(file)


def update_candidate(candidate_id, body):  # noqa: E501
    """Обновить данные кандидата в стажёры

     # noqa: E501

    :param candidate_id: 
    :type candidate_id: str
    :type candidate_id: str
    :param candidate: 
    :type candidate: dict | bytes

    :rtype: Union[CandidateWithId, Tuple[CandidateWithId, int], Tuple[CandidateWithId, int, Dict[str, str]]
    """
    candidate = body
    if connexion.request.is_json:
        candidate = Candidate.from_dict(connexion.request.get_json())  # noqa: E501
    candidate_dict = candidate.to_dict()
    updated_candidate = queries.update_candidate(candidate_id, candidate_dict)
    return updated_candidate
