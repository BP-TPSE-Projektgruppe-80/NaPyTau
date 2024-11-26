import unittest
from argparse import Namespace


class CLIArgumentsUnitTest(unittest.TestCase):
    def test_canBeConstructedFromANamespaceObject(self):
        """Can be constructed from a Namespace object"""
        from napytau.cli.cli_arguments import CLIArguments

        raw_args = Namespace(headless=True, filename="test_filename")
        cli_args = CLIArguments(raw_args)
        self.assertEqual(cli_args.is_headless(), True)
        self.assertEqual(cli_args.get_filename(), "test_filename")

    def test_canBeConstructedFromANamespaceObjectWithNoFilename(self):
        """Can be constructed from a Namespace object with no filename"""
        from napytau.cli.cli_arguments import CLIArguments

        raw_args = Namespace(headless=True, filename=None)
        cli_args = CLIArguments(raw_args)
        self.assertEqual(cli_args.is_headless(), True)
        self.assertEqual(cli_args.get_filename(), None)

    def test_canBeConstructedFromANamespaceObjectWithNoHeadlessFlag(self):
        """Can be constructed from a Namespace object with no headless flag"""
        from napytau.cli.cli_arguments import CLIArguments

        raw_args = Namespace(headless=None, filename="test_filename")
        cli_args = CLIArguments(raw_args)
        self.assertEqual(cli_args.is_headless(), False)
        self.assertEqual(cli_args.get_filename(), "test_filename")

    def test_canBeConstructedFromANamespaceObjectWithNoHeadlessFlagAndNoFilename(self):
        """Can be constructed from a Namespace object with no headless flag and no filename""" # noqa: E501
        from napytau.cli.cli_arguments import CLIArguments

        raw_args = Namespace(headless=None, filename=None)
        cli_args = CLIArguments(raw_args)
        self.assertEqual(cli_args.is_headless(), False)
        self.assertEqual(cli_args.get_filename(), None)

    def test_canDetermineIfTheExecutionHeadless(self):
        """Can determine if the execution is headless"""
        from napytau.cli.cli_arguments import CLIArguments

        raw_args = Namespace(headless=True, filename=None)
        cli_args = CLIArguments(raw_args)
        self.assertEqual(cli_args.is_headless(), True)


if __name__ == "__main__":
    unittest.main()
