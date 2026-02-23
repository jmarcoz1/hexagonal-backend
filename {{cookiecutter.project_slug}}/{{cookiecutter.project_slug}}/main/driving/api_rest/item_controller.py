"""Item REST controller -- driving adapter."""

from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from {{ cookiecutter.project_slug }}.main.application.services.item_service import ItemService
from {{ cookiecutter.project_slug }}.main.boot.containers import Container
from {{ cookiecutter.project_slug }}.main.domain.exceptions import ItemNotFoundException
from {{ cookiecutter.project_slug }}.main.driving.api_rest.schemas import ItemCreateRequest, ItemResponse

router = APIRouter()


@router.get("/items", response_model=list[ItemResponse])
@inject
def list_items(
    item_service: Annotated[ItemService, Depends(Provide[Container.item_service])],
):
    items = item_service.get_all_items()
    return [ItemResponse.model_validate(i.__dict__) for i in items]


@router.get("/items/{item_id}", response_model=ItemResponse)
@inject
def get_item(
    item_id: UUID,
    item_service: Annotated[ItemService, Depends(Provide[Container.item_service])],
):
    try:
        item = item_service.get_item(item_id)
        return ItemResponse.model_validate(item.__dict__)
    except ItemNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )


@router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
@inject
def create_item(
    request: ItemCreateRequest,
    item_service: Annotated[ItemService, Depends(Provide[Container.item_service])],
):
    item = item_service.create_item(name=request.name, description=request.description)
    return ItemResponse.model_validate(item.__dict__)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_item(
    item_id: UUID,
    item_service: Annotated[ItemService, Depends(Provide[Container.item_service])],
):
    try:
        item_service.delete_item(item_id)
    except ItemNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
