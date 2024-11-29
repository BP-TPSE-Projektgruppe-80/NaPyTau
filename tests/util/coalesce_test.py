import unittest
from napytau.util.coalesce import coalesce


class CoalesceUnitTest(unittest.TestCase):
    def test_returnsFirstNonNoneArgument(self):
        """Returns the first non-None argument."""
        self.assertEqual(1, coalesce(None, None, None, 1, 2, 3))

    def test_raisesAValueErrorIfAllArgumentsAreNone(self):
        """Raises a ValueError if all arguments are None."""
        self.assertRaises(ValueError, coalesce, None, None, None)

    def test_raisesAValueErrorIfNoArgumentsAreProvided(self):
        """Returns None if no arguments are provided."""
        self.assertRaises(ValueError, coalesce)


if __name__ == "__main__":
    unittest.main()
