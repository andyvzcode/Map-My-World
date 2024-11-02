import logging
import sys
from typing import Optional

from domain.locations import LocationData
from fastapi import APIRouter, Depends, Request, status, Path
from fastapi.responses import JSONResponse
from responses.success import GenericResponse
from services.locations import LocationService
from utils.builder import location_service_builder

locations_router = APIRouter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info("API locations is starting up")


@locations_router.get(
    "/locations/{location_id}/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
        "content": {
            "application/json": {
                "example": {"id": 1, "latitude": 1.0, "longitude": 1.0}
            }
        },
        "description": "Request was successful."
    },
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "example": {"message": "Location not found"}
            }
        },
        "description": "No location found with the provided ID."
    }
    },
    
    tags=["Locations - Get Location by ID"],
    response_model=GenericResponse
)
async def get(
    location_id: int = Path(..., title="The ID of the location to retrieve"),
    service: LocationService = Depends(location_service_builder),
    ) -> dict:
    response = await service.get(location_id=location_id)
    if not response:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Location not found"})
    return GenericResponse(data=response)
