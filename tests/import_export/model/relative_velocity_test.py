import unittest

from napytau.import_export.model.relative_velocity import RelativeVelocity


class RelativeVelocityUnitTest(unittest.TestCase):
    def test_throwErrorIfNegative(self):
        """A RelativeVelocity should throw an error if the velocity is negative."""
        with self.assertRaises(ValueError):
            RelativeVelocity(-0.1)

    def test_throwErrorIfGreaterThanOne(self):
        """A RelativeVelocity should throw an error if the velocity is greater than 1."""  # noqa E501
        with self.assertRaises(ValueError):
            RelativeVelocity(1.1)

    def test_canBeCreatedWithZero(self):
        """A RelativeVelocity should be able to be created with a velocity of zero."""
        velocity = RelativeVelocity(0)
        self.assertEqual(velocity.get_velocity(), 0)

    def test_canBeCreatedWithOne(self):
        """A RelativeVelocity should be able to be created with a velocity of one."""
        velocity = RelativeVelocity(1)
        self.assertEqual(velocity.get_velocity(), 1)

    def test_equalsItself(self):
        """A RelativeVelocity should be equal to itself."""
        velocity = RelativeVelocity(0.5)
        self.assertEqual(velocity, velocity)

    def test_equalsIdentical(self):
        """Two identical RelativeVelocities should be equal."""
        velocity = RelativeVelocity(0.5)
        other = RelativeVelocity(0.5)
        self.assertEqual(velocity, other)

    def test_notEqualToNone(self):
        """A RelativeVelocity should not be equal to None."""
        velocity = RelativeVelocity(0.5)
        self.assertNotEqual(velocity, None)

    def test_notEqualToDifferentType(self):
        """A RelativeVelocity should not be equal to a different type."""
        velocity = RelativeVelocity(0.5)
        self.assertNotEqual(velocity, 1)

    def test_notEqualToDifferentValue(self):
        """A RelativeVelocity should not be equal to a different RelativeVelocity."""
        velocity = RelativeVelocity(0.5)
        other = RelativeVelocity(0.4)
        self.assertNotEqual(velocity, other)


if __name__ == "__main__":
    unittest.main()
