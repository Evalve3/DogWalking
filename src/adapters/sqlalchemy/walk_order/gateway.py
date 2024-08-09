import datetime
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from src.core.walk_order.entities import WalkOrder
from src.core.walk_order.gateways.walk_order import WalkOrderGateway


class SqlaWalkOrderGateway(WalkOrderGateway):

    def __init__(self, session: Session):
        self.session = session

    def add(self, walk_order: WalkOrder) -> None:
        self.session.add(walk_order)

    def find_by_fields(self, **kwargs) -> List[WalkOrder]:
        """
        Получить заказы по полям сущности
        :param kwargs: поля сущности
        :return: List[WalkOrder]
        """

        if 'walk_time' in kwargs:
            kwargs['walk_time'] = datetime.time(
                hour=kwargs['walk_time'].hour,
                minute=kwargs['walk_time'].minute,
                second=kwargs['walk_time'].second,
                microsecond=kwargs['walk_time'].microsecond
            )
        query = select(WalkOrder)
        conditions = [getattr(WalkOrder, key) == value for key, value in kwargs.items() if hasattr(WalkOrder, key)]

        if conditions:
            stmt = query.where(and_(*conditions))
        else:
            stmt = query  # Если нет условий, просто возвращаем все записи

        result = self.session.execute(stmt).scalars().all()
        return result
