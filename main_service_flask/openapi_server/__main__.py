#!/usr/bin/env python3

import connexion

from flask_cors import CORS

from openapi_server.config import CORS_ORIGINS
from openapi_server import encoder

from openapi_server.database.init_database import init_schema

def main():
    init_schema()

    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    CORS(app.app, resources={r"/*": {
        "origins": CORS_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})
    app.add_api('openapi.yaml',
                arguments={'title': 'Сервис стажёров'},
                pythonic_params=True)

    app.run(port=8081)


if __name__ == '__main__':
    main()
