from abc import abstractmethod, ABC
from typing import List

from src.core.walk_order.entities import WalkOrder


class WalkOrderGateway(ABC):

    @abstractmethod
    def add(self, walk_order: WalkOrder) -> None:
        pass

    @abstractmethod
    def find_by_fields(self, **kwargs) -> List[WalkOrder]:
        """
        Получить заказы по полям сущности
        :param kwargs: поля сущности
        :return: List[WalkOrder]
        """
        pass
