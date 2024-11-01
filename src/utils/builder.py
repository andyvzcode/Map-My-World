import logging
from db.database import get_session_maker
from domain.base import BaseRepository, BaseService, child
from settings.config import Settings

logger = logging.getLogger(__name__)

class BaseBuilder:
    def __init__(self, repository: BaseRepository, Service: BaseService):
        self.repository = repository
        self.Service = Service

    def build(self):
        repository = self.repository(get_session_maker())
        return self.Service(repository)
