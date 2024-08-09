from dataclasses import dataclass, field


@dataclass
class DogWalker:
    id: int = field(init=False)
    name: str
