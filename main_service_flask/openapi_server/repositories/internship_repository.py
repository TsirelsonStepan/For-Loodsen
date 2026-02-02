from openapi_server.database.tables import InternshipDB
from openapi_server.repositories.BaseRepository import BaseRepository


class InternshipRepository(BaseRepository):
    def __init__(self):
        super().__init__(InternshipDB, def_sort_by="position")
