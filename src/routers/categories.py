import logging
import sys

from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse

from domain.categories import CategoryBody
from responses.success import GenericResponse
from services.categories import CategoryService
from utils.builder import category_service_builder

categories_router = APIRouter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info("API categories is starting up")


@categories_router.get(
    "/{category_id}/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {"data": {"id": 1, "name": "Category 1"}}
                }
            },
            "description": "Request was successful.",
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {"example": {"message": "Category not found"}}
            },
            "description": "No category found with the provided ID.",
        },
    },
    response_model=GenericResponse,
)
async def get(
    category_id: int = Path(..., title="The ID of the category to retrieve"),
    service: CategoryService = Depends(category_service_builder),
) -> dict:
    response = await service.get(category_id=category_id)
    if not response:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Category not found"},
        )
    return GenericResponse(data=response)


@categories_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "content": {
                "application/json": {
                    "example": {"data": {"id": 1, "name": "Category 1"}}
                }
            },
            "description": "Category was created successfully.",
        }
    },
    response_model=GenericResponse,
)
async def create(
    category: CategoryBody,
    service: CategoryService = Depends(category_service_builder),
) -> GenericResponse:
    response = await service.save(category)
    return GenericResponse(data=response)


@categories_router.put(
    "/{category_id}/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {"data": {"id": 1, "name": "Category 1"}}
                }
            },
            "description": "Category was updated successfully.",
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {"example": {"message": "Category not found"}}
            },
            "description": "No category found with the provided ID.",
        },
    },
    response_model=GenericResponse,
)
async def update(
    category: CategoryBody,
    category_id: int = Path(..., title="The ID of the category to update"),
    service: CategoryService = Depends(category_service_builder),
) -> GenericResponse:
    response = await service.update(category_id, category)
    if not response:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Category not found"},
        )
    return GenericResponse(data=response)


@categories_router.delete(
    "/{category_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Category was deleted successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {"example": {"message": "Category not found"}}
            },
            "description": "No category found with the provided ID.",
        },
    },
)
async def delete(
    category_id: int = Path(..., title="The ID of the category to delete"),
    service: CategoryService = Depends(category_service_builder),
) -> JSONResponse:
    response = await service.get(category_id)
    if not response:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Category not found"},
        )
    await service.delete(category_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)


@categories_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {"id": 1, "name": "Category 1"},
                            {"id": 2, "name": "Category 2"},
                        ]
                    }
                }
            },
            "description": "Request was successful.",
        }
    },
    response_model=GenericResponse,
)
async def list(
    service: CategoryService = Depends(category_service_builder),
) -> GenericResponse:
    response = await service.list()
    return GenericResponse(data=response)
