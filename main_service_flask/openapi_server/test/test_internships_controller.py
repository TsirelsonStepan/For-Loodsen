import unittest

from flask import json

from openapi_server.models.add_internship200_response import AddInternship200Response  # noqa: E501
from openapi_server.models.get_internships200_response import GetInternships200Response  # noqa: E501
from openapi_server.models.internship import Internship  # noqa: E501
from openapi_server.models.internship_with_id import InternshipWithId  # noqa: E501
from openapi_server.test import BaseTestCase


class TestInternshipsController(BaseTestCase):
    """InternshipsController integration test stubs"""

    def test_add_internship(self):
        """Test case for add_internship

        Добавить запрос на стажёра
        """
        internship = {"skills":"skills","education":"education","hoursPerWeek":21,"employmentType":"в офисе","description":"description","position":"position","department":"department","status":"просмотрено"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/internships',
            method='POST',
            headers=headers,
            data=json.dumps(internship),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_internship(self):
        """Test case for delete_internship

        Удалить запрос на стажёра
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/internships/{internship_id}'.format(internship_id='f81d4fae-7dec-11d0-a765-00a0c91e6bf6'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_internshipby_id(self):
        """Test case for get_internshipby_id

        Получить стажировку по ID
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/internships/{internship_id}'.format(internship_id='f81d4fae-7dec-11d0-a765-00a0c91e6bf6'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_internships(self):
        """Test case for get_internships

        Получить список всех стажировок
        """
        query_string = [('position', 'Junior Backend Developer'),
                        ('department', 'ДРВПО'),
                        ('limit', 10),
                        ('offset', 0),
                        ('sortBy', 'name'),
                        ('sortOrder', 'sort_order_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/internships',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_internship(self):
        """Test case for update_internship

        Обновить запрос на стажёра
        """
        internship = {"skills":"skills","education":"education","hoursPerWeek":21,"employmentType":"в офисе","description":"description","position":"position","department":"department","status":"просмотрено"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/internships/{internship_id}'.format(internship_id='f81d4fae-7dec-11d0-a765-00a0c91e6bf6'),
            method='PUT',
            headers=headers,
            data=json.dumps(internship),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
