import unittest
from napytau.util.coalesce import coalesce


class CoalesceUnitTest(unittest.TestCase):
    def test_returnsFirstNonNoneArgument(self):
        """Returns the first non-None argument."""
        self.assertEqual(1, coalesce(None, None, None, 1, 2, 3))

    def test_returnsNoneIfAllArgumentsAreNone(self):
        """Returns None if all arguments are None."""
        self.assertIsNone(coalesce(None, None, None))

    def test_returnsNoneIfNoArgumentsAreProvided(self):
        """Returns None if no arguments are provided."""
        self.assertIsNone(coalesce())


if __name__ == "__main__":
    unittest.main()
