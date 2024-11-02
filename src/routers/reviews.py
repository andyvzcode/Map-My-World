import logging
import sys

from aiocache import cached
from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse

from domain.reviews import ReviewBody
from responses.success import GenericResponse
from services.reviews import ReviewService
from utils.builder import review_service_builder

reviews_router = APIRouter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info("API reviews is starting up")


@reviews_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "id": 1,
                            "category_id": 1,
                            "location_id": 1,
                            "last_reviewed": "2021-01-01",
                        }
                    }
                }
            },
            "description": "Category was created successfully.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {"example": {"message": "Invalid request"}}
            },
            "description": "Request was invalid.",
        },
    },
    response_model=GenericResponse,
)
async def create(
    review: ReviewBody,
    service: ReviewService = Depends(review_service_builder),
) -> dict:
    response = await service.save(review=review)
    if not response:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Invalid request"},
        )
    return GenericResponse(data=response)


@reviews_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {
                                "id": 1,
                                "category_id": 1,
                                "location_id": 1,
                                "last_reviewed": "2021-01-01",
                            }
                        ]
                    }
                }
            },
            "description": "List of reviews",
        }
    },
    response_model=GenericResponse,
)
@cached(ttl=60 * 5)
async def list(service: ReviewService = Depends(review_service_builder)) -> dict:
    response = await service.list()
    return GenericResponse(data=response)
