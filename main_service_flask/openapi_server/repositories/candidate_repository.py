from openapi_server.database.tables import CandidateDB
from openapi_server.repositories.BaseRepository import BaseRepository


class CandidateRepository(BaseRepository):
    def __init__(self):
        super().__init__(CandidateDB, def_sort_by="name")
