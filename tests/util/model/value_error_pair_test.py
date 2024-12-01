import unittest

from napytau.util.model.value_error_pair import ValueErrorPair


class ValueErrorPairUnitTest(unittest.TestCase):
    def test_equalsItself(self):
        """A ValueErrorPair should be equal to itself."""
        pair = ValueErrorPair(1, 2)
        self.assertEqual(pair, pair)

    def test_equalsIdentical(self):
        """Two identical ValueErrorPairs should be equal."""
        pair = ValueErrorPair(1, 2)
        other = ValueErrorPair(1, 2)
        self.assertEqual(pair, other)

    def test_notEqualToNone(self):
        """A ValueErrorPair should not be equal to None."""
        pair = ValueErrorPair(1, 2)
        self.assertNotEqual(pair, None)

    def test_notEqualToDifferentType(self):
        """A ValueErrorPair should not be equal to a different type."""
        pair = ValueErrorPair(1, 2)
        self.assertNotEqual(pair, 1)

    def test_notEqualToDifferentValue(self):
        """A ValueErrorPair should not be equal to a different ValueErrorPair."""
        pair = ValueErrorPair(1, 2)
        other = ValueErrorPair(2, 1)
        self.assertNotEqual(pair, other)


if __name__ == "__main__":
    unittest.main()
