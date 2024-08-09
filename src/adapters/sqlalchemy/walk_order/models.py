from sqlalchemy import Integer, String, Column, Table, Date, Time, ForeignKey

from src.adapters.sqlalchemy.base import metadata_obj

walk_order = Table(
    "walk_order",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("apartment_number", Integer),
    Column("dog_name", String()),
    Column("dog_breed", String()),
    Column("walk_date", Date()),
    Column("walk_time", Time()),
    Column("walk_duration", Integer),
    Column("walker_id", Integer, ForeignKey('walker.id'))
)


