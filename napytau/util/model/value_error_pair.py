class ValueErrorPair[T]:
    def __init__(self, value: T, error: T):
        self.value = value
        self.error = error

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ValueErrorPair):
            return NotImplemented
        return bool(self.value == other.value and self.error == other.error)
