import datetime

import pytest
from unittest.mock import MagicMock, Mock
from datetime import date

from src.core.abc.use_case import SuccessResult
from src.core.walk_order.usecases.walk_orders_by_date import WalkOrdersByDate, WalkOrdersByDateInputDTO


@pytest.fixture
def walk_order_gateway():
    return MagicMock()


@pytest.fixture
def walk_orders_by_date_use_case(walk_order_gateway):
    return WalkOrdersByDate(
        walk_order_gateway=walk_order_gateway
    )


@pytest.fixture
def walk_orders_by_date_input_dto():
    return WalkOrdersByDateInputDTO(
        date=date(2024, 8, 10)
    )


@pytest.fixture
def walk_order_list():
    return [
        Mock(
            id=1,
            apartment_number=101,
            dog_name="Buddy",
            dog_breed="Golden Retriever",
            walk_date=date(2024, 8, 10),
            walk_time=datetime.time(10, 0),
            walk_duration=30,
            walker_id=1
        ),
        Mock(
            id=2,
            apartment_number=202,
            dog_name="Max",
            dog_breed="Beagle",
            walk_date=date(2024, 8, 10),
            walk_time=datetime.time(11, 0),
            walk_duration=45,
            walker_id=2
        )
    ]


def test_walk_orders_by_date_success(walk_orders_by_date_use_case, walk_order_gateway, walk_orders_by_date_input_dto,
                                     walk_order_list):
    # Arrange
    walk_order_gateway.find_by_fields.return_value = walk_order_list

    # Act
    result = walk_orders_by_date_use_case.execute(walk_orders_by_date_input_dto)

    # Assert
    assert isinstance(result, SuccessResult)
    assert len(result.data.walk_orders) == len(walk_order_list)
    assert result.data.walk_orders == walk_order_list
    walk_order_gateway.find_by_fields.assert_called_once_with(walk_date=walk_orders_by_date_input_dto.date)


def test_walk_orders_by_date_no_orders(walk_orders_by_date_use_case, walk_order_gateway, walk_orders_by_date_input_dto):
    # Arrange
    walk_order_gateway.find_by_fields.return_value = []

    # Act
    result = walk_orders_by_date_use_case.execute(walk_orders_by_date_input_dto)

    # Assert
    assert isinstance(result, SuccessResult)
    assert len(result.data.walk_orders) == 0
    walk_order_gateway.find_by_fields.assert_called_once_with(walk_date=walk_orders_by_date_input_dto.date)
