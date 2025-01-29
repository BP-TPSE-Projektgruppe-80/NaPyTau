from abc import abstractmethod
from typing import List


class Writer[T]:
    """
    The Writer class is an abstract class that defines the interface for writing
     data to some source.
    It's subclasses determine how to write data to a specific source.
    By instantiating the TypeVar T, the subclasses define how
    the source must be specified.
    """

    @staticmethod
    @abstractmethod
    def write_rows(resource_identifier: T, rows: List[str]) -> None:
        pass
