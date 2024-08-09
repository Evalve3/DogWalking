from dataclasses import dataclass
import datetime
from typing import List

from src.core.abc.use_case import UseCase, SuccessResult, FailResult
from src.core.walk_order.entities import WalkOrder
from src.core.walk_order.gateways.walk_order import WalkOrderGateway


@dataclass
class WalkOrdersByDateInputDTO:
    date: datetime.date


@dataclass
class WalkOrdersByDateOutputDTO:
    walk_orders: List[WalkOrder]


class WalkOrdersByDate(UseCase[WalkOrdersByDateInputDTO, WalkOrdersByDateOutputDTO]):

    def __init__(self,
                 walk_order_gateway: WalkOrderGateway,
                 ):
        self.walk_order_gateway = walk_order_gateway

    def execute(self, dto: WalkOrdersByDateInputDTO) -> SuccessResult | FailResult:
        walk_orders = self.walk_order_gateway.find_by_fields(
            walk_date=dto.date
        )
        return SuccessResult(data=WalkOrdersByDateOutputDTO(walk_orders=walk_orders))
