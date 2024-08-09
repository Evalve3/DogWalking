from typing import Protocol


class UoW(Protocol):
    """Unit of work pattern protocol."""

    def commit(self):
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError
