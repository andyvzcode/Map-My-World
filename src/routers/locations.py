import logging
import sys

from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse

from domain.locations import LocationBody, LocationData
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
                    "example": {"data": {"id": 1, "latitude": 1.0, "longitude": 1.0}}
                }
            },
            "description": "Request was successful.",
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {"example": {"message": "Location not found"}}
            },
            "description": "No location found with the provided ID.",
        },
    },
    tags=["Locations - Get Location by ID"],
    response_model=GenericResponse,
)
async def get(
    location_id: int = Path(..., title="The ID of the location to retrieve"),
    service: LocationService = Depends(location_service_builder),
) -> dict:
    response = await service.get(location_id=location_id)
    if not response:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Location not found"},
        )
    return GenericResponse(data=response)


@locations_router.get(
    "/locations/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": [{"id": 1, "latitude": 1.0, "longitude": 1.0}]
                }
            },
            "description": "Request was successful.",
        }
    },
    tags=["Locations - List Locations"],
    response_model=GenericResponse,
)
async def list(
    service: LocationService = Depends(location_service_builder),
) -> GenericResponse:
    response = await service.list()
    return GenericResponse(data=response)


@locations_router.post(
    "/locations/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "content": {
                "application/json": {
                    "example": {"data": {"id": 1, "latitude": 1.0, "longitude": 1.0}}
                }
            },
            "description": "Request was successful.",
        }
    },
    tags=["Locations - Create Location"],
    response_model=GenericResponse,
)
async def create(
    location: LocationBody,
    service: LocationService = Depends(location_service_builder),
) -> GenericResponse:
    response = await service.save(location)
    return GenericResponse(data=response)


@locations_router.put(
    "/locations/{location_id}/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {"data": {"id": 1, "latitude": 1.0, "longitude": 1.0}}
                }
            },
            "description": "Request was successful.",
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {"example": {"message": "Location not found"}}
            },
            "description": "No location found with the provided ID.",
        },
    },
    tags=["Locations - Update Location"],
    response_model=GenericResponse,
)
async def update(
    location: LocationBody,
    location_id: int = Path(..., title="The ID of the location to update"),
    service: LocationService = Depends(location_service_builder),
) -> GenericResponse:
    response = await service.update(location_id, location)
    if not response:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Location not found"},
        )
    return GenericResponse(data=response)


@locations_router.delete(
    "/locations/{location_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Request was successful.",
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {"example": {"message": "Location not found"}}
            },
            "description": "No location found with the provided ID.",
        },
    },
    tags=["Locations - Delete Location"],
)
async def delete(
    location_id: int = Path(..., title="The ID of the location to delete"),
    service: LocationService = Depends(location_service_builder),
) -> None:
    response = await service.get(location_id)
    if not response:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Location not found"},
        )
    await service.delete(location_id)
    return None
