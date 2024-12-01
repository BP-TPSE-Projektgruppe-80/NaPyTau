from os import walk
from os.path import isdir
from typing import List, Callable
from re import match as regex_match

from napytau.ingest.crawler.crawler import Crawler


class FileCrawler[T](Crawler[str, T]):
    """
    The FileCrawler crawls files from a directory tree. Starting from a base directory,
    it searches for files with names specified in the needles list.
    By providing the generic type T, the FileCrawler allows the user to specify
    the data structure, the found filenames will be stored in.
    """

    file_name_patterns: List[str]
    """
    A list of file names to search for in the directory tree.
    The FileCrawler will search for files matching the provided regular expressions.
    """

    return_type_factory: Callable[[List[str]], T]
    """A factory function to create the return type from the found filenames."""

    def __init__(
        self,
        file_name_patterns: List[str],
        return_type_factory: Callable[[List[str]], T],
    ):
        self.file_name_patterns = file_name_patterns
        self.return_type_factory = return_type_factory

    def crawl(self, directory_path: str) -> List[T]:
        if not isdir(directory_path):
            raise ValueError(f"Directory path {directory_path} is not a directory.")

        crawled_files = []

        directory_tree = walk(directory_path)
        for root_path, directories, files in directory_tree:
            crawled_files_in_directory = []
            for file in files:
                if any(
                    regex_match(file_name_pattern, file)
                    for file_name_pattern in self.file_name_patterns
                ):
                    crawled_files_in_directory.append(f"{root_path}/{file}")

            if len(crawled_files_in_directory) > 0:
                crawled_files.append(
                    self.return_type_factory(crawled_files_in_directory)
                )

        return crawled_files
