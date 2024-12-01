class RelativeVelocity:
    velocity: float

    def __init__(self, raw_velocity: float):
        """raw_velocity: the measure velocity relative to the speed of light"""
        if raw_velocity < 0:
            raise ValueError("Velocity cannot be negative")

        if raw_velocity > 1:
            raise ValueError("Velocity cannot be greater than the speed of light")

        self.velocity = raw_velocity

    def get_velocity(self) -> float:
        return self.velocity

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RelativeVelocity):
            return NotImplemented
        return self.velocity == other.velocity
