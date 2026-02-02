import unittest

from flask import json

from openapi_server.models.candidate import Candidate  # noqa: E501
from openapi_server.models.candidate_with_id import CandidateWithId  # noqa: E501
from openapi_server.models.get_candidates200_response import GetCandidates200Response  # noqa: E501
from openapi_server.test import BaseTestCase


class TestCandidatesController(BaseTestCase):
    """CandidatesController integration test stubs"""

    def test_add_candidate(self):
        """Test case for add_candidate

        Добавить кандидата в стажёры
        """
        candidate = {"skills":"skills","pathToResume":"pathToResume","education":"education","hoursPerWeek":21,"phone":"+77777777777","employmentType":"в офисе","name":"Иванов Иван Иванович","links":"links","position":"position","experience":"experience","email":"example@example.com"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/candidates',
            method='POST',
            headers=headers,
            data=json.dumps(candidate),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_candidate(self):
        """Test case for delete_candidate

        Удалить кандидата в стажёры
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/candidates/{candidate_id}'.format(candidate_id='f81d4fae-7dec-11d0-a765-00a0c91e6bf6'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_export_candidates(self):
        """Test case for export_candidates

        Экспортировать таблицу стажёров из базы данных в CSV файл
        """
        query_string = [('candidateName', ''),
                        ('candidatePhone', ''),
                        ('candidateEmail', ''),
                        ('candidateSkills', ['[]']),
                        ('candidatePosition', ''),
                        ('candidateHours', 56),
                        ('candidateEmploymentType', 'candidate_employment_type_example'),
                        ('limit', 10),
                        ('offset', 0),
                        ('sortBy', 'name'),
                        ('sortOrder', 'sort_order_example')]
        headers = { 
            'Accept': 'text/csv',
        }
        response = self.client.open(
            '/api/v1/candidates/external',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_candidateby_id(self):
        """Test case for get_candidateby_id

        Получить кандидата в стажеры по ID
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/candidates/{candidate_id}'.format(candidate_id='f81d4fae-7dec-11d0-a765-00a0c91e6bf6'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_candidates(self):
        """Test case for get_candidates

        Получить список всех кандидатов в стажёры
        """
        query_string = [('candidateName', ''),
                        ('candidatePhone', ''),
                        ('candidateEmail', ''),
                        ('candidateSkills', ['[]']),
                        ('candidatePosition', ''),
                        ('candidateHours', 56),
                        ('candidateEmploymentType', 'candidate_employment_type_example'),
                        ('limit', 10),
                        ('offset', 0),
                        ('sortBy', 'name'),
                        ('sortOrder', 'sort_order_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/candidates',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_import_candidates(self):
        """Test case for import_candidates

        Импортировать в базу данных стажёров из CSV файла
        """
        headers = { 
            'Content-Type': 'multipart/form-data',
        }
        data = dict(file='/path/to/file')
        response = self.client.open(
            '/api/v1/candidates/external',
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_candidate(self):
        """Test case for update_candidate

        Обновить данные кандидата в стажёры
        """
        candidate = {"skills":"skills","pathToResume":"pathToResume","education":"education","hoursPerWeek":21,"phone":"+77777777777","employmentType":"в офисе","name":"Иванов Иван Иванович","links":"links","position":"position","experience":"experience","email":"example@example.com"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/candidates/{candidate_id}'.format(candidate_id='f81d4fae-7dec-11d0-a765-00a0c91e6bf6'),
            method='PUT',
            headers=headers,
            data=json.dumps(candidate),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
