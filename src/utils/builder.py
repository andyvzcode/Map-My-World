import logging

from db.database import get_session_maker
from repositories.categories import CategoryRepository
from repositories.locations import LocationRepository
from repositories.reviews import ReviewRepository
from services.categories import CategoryService
from services.locations import LocationService
from services.reviews import ReviewService

logger = logging.getLogger(__name__)


def location_service_builder():
    repository = LocationRepository(get_session_maker())
    return LocationService(repository)


def category_service_builder():
    repository = CategoryRepository(get_session_maker())
    return CategoryService(repository)


def review_service_builder():
    repository = ReviewRepository(get_session_maker())
    return ReviewService(repository)
