from abc import ABC, abstractmethod

from src.core.walker.entities import DogWalker


class WalkerGateway(ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> DogWalker:
        pass
