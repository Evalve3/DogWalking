from dataclasses import dataclass, field
import datetime


@dataclass
class WalkOrder:
    id: int = field(init=False)
    apartment_number: int
    dog_name: str
    dog_breed: str
    walk_date: datetime.date
    walk_time: datetime.time  # Use InitVar for initial value
    walk_duration: int  # minutes
    walker_id: int

