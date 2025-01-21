from napytau.util.model.value_error_pair import ValueErrorPair
from dataclasses import dataclass
from typing import List, Iterator
import numpy as np


@dataclass
class ValueErrorPairCollection[T]:
    elements: List[ValueErrorPair[T]]

    def __getitem__(self, key: int) -> ValueErrorPair[T]:
        return self.elements[key]

    def __iter__(self) -> Iterator[ValueErrorPair[T]]:
        return iter(self.elements)

    def get_values(self) -> np.ndarray:
        values: np.ndarray = np.ndarray(shape=len(self.elements), dtype=float)

        for i in range(len(self.elements)):
            values[i] = self.elements[i].value  # type: ignore

        return values

    def get_errors(self) -> np.ndarray:
        errors: np.ndarray = np.zeros(shape=len(self.elements), dtype=float)

        for i in range(len(self.elements)):
            errors[i] = self.elements[i].error  # type: ignore

        return errors
