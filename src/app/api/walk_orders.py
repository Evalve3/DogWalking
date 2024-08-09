import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, validator

from src.app.depends import new_walk_order_gateway, new_uow, new_walker_gateway, new_walker_orders_validator
from src.core.abc.database import UoW
from src.core.abc.use_case import FailResult
from src.core.walk_order.gateways.walk_order import WalkOrderGateway
from src.core.walk_order.usecases.add_walk_order import AddWalkOrder, WalkOrderInputDTO, WalkOrderOutputDTO
from src.core.walk_order.usecases.walk_orders_by_date import WalkOrdersByDate, WalkOrdersByDateInputDTO
from src.core.walk_order.walk_order_validator import WalkOrderValidator
from src.core.walker.gateways.walker_gateway import WalkerGateway

walk_order_router = APIRouter()


class AddWalkOrderSchema(BaseModel):
    apartment_number: int
    dog_name: str
    dog_breed: str
    walk_date: datetime.date
    walk_time: datetime.time
    walk_duration_in_minutes: int
    walker_name: str

    @validator('walk_time')
    def validate_time(cls, value):
        if value.second != 0 or value.microsecond != 0:
            raise ValueError('walk_time should only contain hours and minutes')
        return value


@walk_order_router.post('/')
def add_walk_order(
        body: AddWalkOrderSchema,
        walk_order_gateway: WalkOrderGateway = Depends(new_walk_order_gateway),
        uow: UoW = Depends(new_uow),
        walker_gateway: WalkerGateway = Depends(new_walker_gateway),
        walk_validator: WalkOrderValidator = Depends(new_walker_orders_validator)
) -> WalkOrderOutputDTO:  # При необходимости можно добавить слой презентеров и мапить в дто слоя фаст апи
    uc = AddWalkOrder(
        walk_order_gateway=walk_order_gateway,
        uow=uow,
        walker_gateway=walker_gateway,
        walk_validator=walk_validator
    )
    dto = WalkOrderInputDTO(
        apartment_number=body.apartment_number,
        dog_name=body.dog_name,
        dog_breed=body.dog_breed,
        walk_date=body.walk_date,
        walk_time=body.walk_time,
        walk_duration=body.walk_duration_in_minutes,
        walker_name=body.walker_name
    )
    result = uc.execute(dto)

    if isinstance(result, FailResult):
        raise HTTPException(
            status_code=result.status_code,
            detail=result.message
        )

    return result.data


@walk_order_router.get('/')
def get_walk_orders(
        date: datetime.date = Query(None, description="The date to retrieve walk orders for"),
        walk_order_gateway: WalkOrderGateway = Depends(new_walk_order_gateway)
):
    uc = WalkOrdersByDate(
        walk_order_gateway=walk_order_gateway
    )
    dto = WalkOrdersByDateInputDTO(
        date=date
    )

    result = uc.execute(dto)

    if isinstance(result, FailResult):
        raise HTTPException(
            status_code=result.status_code,
            detail=result.message
        )

    return result.data
