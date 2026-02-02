import unittest

from flask import json

from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_parse_file(self):
        """Test case for parse_file

        
        """
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data',
        }
        data = dict(file='/path/to/file')
        response = self.client.open(
            '/FileParser',
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
