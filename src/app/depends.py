import os
from functools import partial
from typing import Iterable

from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, Session

from src.adapters.sqlalchemy import walker
from src.adapters.sqlalchemy.walk_order.gateway import SqlaWalkOrderGateway
from src.adapters.sqlalchemy.walker.gateway import SqlaWalkerGateway
from src.core.abc.database import UoW
from src.core.walk_order.gateways.walk_order import WalkOrderGateway
from src.core.walk_order.walk_order_validator import WalkOrderValidator
from src.core.walker.entities import DogWalker
from src.core.walker.gateways.walker_gateway import WalkerGateway


def create_session_maker():
    db_uri = os.getenv("DB_URL")

    if not db_uri:
        raise ValueError("DB_URI env variable is not set")

    engine = create_engine(
        db_uri,
        echo=True
    )
    return sessionmaker(engine, autoflush=False, expire_on_commit=False)


def new_session() -> Session:
    session_maker = create_session_maker()
    with session_maker() as session:
        yield session


def new_walk_order_gateway(session: Session = Depends(new_session)) -> WalkOrderGateway:
    yield SqlaWalkOrderGateway(session)


def new_uow(session: Session = Depends(new_session)) -> UoW:
    return session


def new_walker_gateway(session: Session = Depends(new_session)) -> WalkerGateway:
    yield SqlaWalkerGateway(session)


def new_walker_orders_validator() -> WalkOrderValidator:
    yield WalkOrderValidator()


def init_dependencies(app: FastAPI):
    session = next(new_session())

    try:
        # Проверяем, есть ли записи в таблице
        walker_count = session.query(walker).count()
    except NoResultFound:
        walker_count = 0

    # Если таблица пуста, создаем две новые записи
    if walker_count == 0:
        walker1 = DogWalker(name="Антон")
        walker2 = DogWalker(name="Пётр")
        session.add(walker1)
        session.add(walker2)
        session.commit()


