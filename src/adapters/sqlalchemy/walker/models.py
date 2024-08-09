from sqlalchemy import Integer, String, Column, Table

from src.adapters.sqlalchemy.base import metadata_obj

walker = Table(
    "walker",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String()),
)


