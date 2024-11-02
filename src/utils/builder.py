import logging
from db.database import get_session_maker
from domain.base import BaseRepository, BaseService
from repositories.locations import LocationRepository
from services.locations import LocationService 

logger = logging.getLogger(__name__)

def location_service_builder():
    repository = LocationRepository(get_session_maker())
    return LocationService(repository)
