from dataclasses import dataclass
import datetime

from src.core.abc.database import UoW
from src.core.abc.use_case import UseCase, SuccessResult, FailResult
from src.core.walk_order.entities import WalkOrder
from src.core.walk_order.gateways.walk_order import WalkOrderGateway
from src.core.walk_order.walk_order_validator import WalkOrderValidator
from src.core.walker.gateways.walker_gateway import WalkerGateway


@dataclass
class WalkOrderInputDTO:
    apartment_number: int
    dog_name: str
    dog_breed: str
    walk_date: datetime.date
    walk_time: datetime.time
    walk_duration: int
    walker_name: str


@dataclass
class WalkOrderOutputDTO:
    id: int


class AddWalkOrder(UseCase[WalkOrderInputDTO, WalkOrderOutputDTO]):

    def __init__(self,
                 walk_order_gateway: WalkOrderGateway,
                 uow: UoW,
                 walker_gateway: WalkerGateway,
                 walk_validator: WalkOrderValidator
                 ):
        self.walk_order_gateway = walk_order_gateway
        self.uow = uow
        self.walker_gateway = walker_gateway
        self.walk_validator = walk_validator

    def execute(self, dto: WalkOrderInputDTO) -> SuccessResult | FailResult:

        if not self.walk_validator.validate_walk_time(
                time=dto.walk_time
        ):
            return FailResult(
                message='Некорректное время начала прогулки',
                status_code=400
            )

        if not self.walk_validator.validate_walk_duration(
                duration=dto.walk_duration
        ):
            return FailResult(
                message='Некорректное длительность прогулки',
                status_code=400
            )

        walker = self.walker_gateway.get_by_name(
            name=dto.walker_name
        )

        walker_busy = bool(self.walk_order_gateway.find_by_fields(
            walker_id=walker.id,
            walk_date=dto.walk_date,
            walk_time=dto.walk_time
        ))

        if walker_busy:
            return FailResult(
                message='Время занято',
                status_code=400
            )

        walk_order = WalkOrder(
            apartment_number=dto.apartment_number,
            dog_name=dto.dog_name,
            dog_breed=dto.dog_breed,
            walk_date=dto.walk_date,
            walk_time=dto.walk_time,
            walk_duration=dto.walk_duration,
            walker_id=walker.id
        )

        self.walk_order_gateway.add(
            walk_order=walk_order
        )

        self.uow.commit()

        result = WalkOrderOutputDTO(
            id=walk_order.id
        )

        return SuccessResult(
            data=result
        )
