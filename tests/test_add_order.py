import pytest
from unittest.mock import MagicMock, Mock
from datetime import date, time

from src.core.abc.use_case import FailResult, SuccessResult
from src.core.walk_order.usecases.add_walk_order import WalkOrderInputDTO, AddWalkOrder


@pytest.fixture
def walk_order_gateway():
    return MagicMock()


@pytest.fixture
def uow():
    return MagicMock()


@pytest.fixture
def walker_gateway():
    return MagicMock()


@pytest.fixture
def walk_validator():
    return MagicMock()


@pytest.fixture
def add_walk_order_use_case(walk_order_gateway, uow, walker_gateway, walk_validator):
    return AddWalkOrder(
        walk_order_gateway=walk_order_gateway,
        uow=uow,
        walker_gateway=walker_gateway,
        walk_validator=walk_validator
    )


@pytest.fixture
def walk_order_input_dto():
    return WalkOrderInputDTO(
        apartment_number=101,
        dog_name="Buddy",
        dog_breed="Golden Retriever",
        walk_date=date(2024, 8, 10),
        walk_time=time(10, 0),
        walk_duration=30,
        walker_name="John Doe"
    )


@pytest.fixture
def walker():
    return Mock(id=1, name="John Doe")


def test_add_walk_order_success(add_walk_order_use_case, walk_order_gateway, uow, walker_gateway, walk_validator,
                                walk_order_input_dto, walker):
    # Arrange
    def foo(walk_order):
        walk_order.id = 42

    walk_validator.validate_walk_time.return_value = True
    walk_validator.validate_walk_duration.return_value = True
    walker_gateway.get_by_name.return_value = walker
    walk_order_gateway.find_by_fields.return_value = []
    walk_order_gateway.add = foo

    # Act
    result = add_walk_order_use_case.execute(walk_order_input_dto)

    # Assert
    assert isinstance(result, SuccessResult)
    uow.commit.assert_called_once()
    assert result.data.id == 42


def test_add_walk_order_invalid_time(add_walk_order_use_case, walk_validator, walk_order_input_dto):
    # Arrange
    walk_validator.validate_walk_time.return_value = False

    # Act
    result = add_walk_order_use_case.execute(walk_order_input_dto)

    # Assert
    assert isinstance(result, FailResult)
    assert result.message == 'Некорректное время начала прогулки'
    assert result.status_code == 400


def test_add_walk_order_invalid_duration(add_walk_order_use_case, walk_validator, walk_order_input_dto):
    # Arrange
    walk_validator.validate_walk_time.return_value = True
    walk_validator.validate_walk_duration.return_value = False

    # Act
    result = add_walk_order_use_case.execute(walk_order_input_dto)

    # Assert
    assert isinstance(result, FailResult)
    assert result.message == 'Некорректное длительность прогулки'
    assert result.status_code == 400


def test_add_walk_order_walker_busy(add_walk_order_use_case, walk_order_gateway, walker_gateway, walk_order_input_dto,
                                    walker, walk_validator):
    # Arrange
    walk_validator.validate_walk_time.return_value = True
    walk_validator.validate_walk_duration.return_value = True
    walker_gateway.get_by_name.return_value = walker
    walk_order_gateway.find_by_fields.return_value = [MagicMock()]

    # Act
    result = add_walk_order_use_case.execute(walk_order_input_dto)

    # Assert
    assert isinstance(result, FailResult)
    assert result.message == 'Время занято'
    assert result.status_code == 400
