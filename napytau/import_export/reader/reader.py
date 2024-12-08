from abc import abstractmethod
from typing import List


class Reader[T]:
    """
    The Reader class is an abstract class that defines the interface for reading
     data from some source.
    It's subclasses determine how to read data from a specific source.
    By instantiating the TypeVar T, the subclasses define how
    the source must be specified.
    """

    @staticmethod
    @abstractmethod
    def read_rows(resource_identifier: T) -> List[str]:
        pass
