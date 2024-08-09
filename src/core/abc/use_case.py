from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Protocol, TypeVar, Optional, Generic

InputDTO = TypeVar('InputDTO')

OutputDTO = TypeVar('OutputDTO')


@dataclass
class SuccessResult:
    data: Optional[OutputDTO]
    status_code: int = 200


@dataclass
class FailResult:
    message: str
    exception: Exception = field(metadata={"hidden": True}, default=None)
    status_code: int = 500


class UseCase(Generic[InputDTO, OutputDTO]):
    @abstractmethod
    def execute(self, dto: InputDTO) -> SuccessResult | FailResult:
        pass
