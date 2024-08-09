from sqlalchemy import MetaData
from sqlalchemy.orm import registry

from src.adapters.sqlalchemy.walk_order.models import walk_order
from src.adapters.sqlalchemy.walker.models import walker
from src.core.walk_order.entities import WalkOrder
from src.core.walker.entities import DogWalker


mapper_registry = registry()
mapper_registry.map_imperatively(WalkOrder, walk_order)
mapper_registry.map_imperatively(DogWalker, walker)
