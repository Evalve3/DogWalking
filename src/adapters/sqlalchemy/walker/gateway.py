from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.walker.entities import DogWalker
from src.core.walker.gateways.walker_gateway import WalkerGateway


class SqlaWalkerGateway(WalkerGateway):

    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, name: str) -> DogWalker:
        """
        Получить сущность по имени
        :param name: имя сущности
        :return: DogWalker
        """
        stmt = select(DogWalker).where(DogWalker.name == name)
        result = self.session.execute(stmt).scalar_one()
        return result
