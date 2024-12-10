from abc import abstractmethod
from typing import List


class Crawler[T, U]:
    """
    The Crawler class is an abstract class that defines the interface
    for crawling data from some source.
    It's subclasses determine how to crawl data from a specific source.
    By instantiating the TypeVar T, the subclasses define
    how the source must be specified.
    """

    @abstractmethod
    def crawl(self, resource_identifier: T) -> List[U]:
        """
        Crawls from a base resource identifier and returns a list of lists of resources.
        This is intended to allow the user to specify a base resource identifier
         and have the system discover all necessary data to be ingested.
        """
        pass
