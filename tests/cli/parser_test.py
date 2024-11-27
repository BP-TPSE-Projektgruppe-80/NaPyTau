import unittest
from argparse import Namespace
from unittest.mock import MagicMock, patch


def set_up_mocks() -> (MagicMock, MagicMock, MagicMock):
    argparse_module_mock = MagicMock()
    argument_parser_mock = MagicMock()
    argument_parser_mock.add_argument = MagicMock()
    argparse_module_mock.ArgumentParser.return_value = argument_parser_mock
    cli_arguments_module_mock = MagicMock()
    cli_arguments_module_mock.CLIArguments = MagicMock()
    return argparse_module_mock, argument_parser_mock, cli_arguments_module_mock


class ParserUnitTest(unittest.TestCase):
    def test_createsAnArgumentParserInstanceAndConfiguresIt(self):
        """Creates an ArgumentParser instance and configures it"""
        argparse_module_mock, argument_parser_mock, cli_arguments_module_mock = (
            set_up_mocks()
        )
        with patch.dict(
            "sys.modules",
            {
                "argparse": argparse_module_mock,
                "napytau.cli.cli_arguments": cli_arguments_module_mock,
            },
        ):
            from napytau.cli.parser import parse_cli_arguments

            parse_cli_arguments()
            self.assertEqual(len(argument_parser_mock.add_argument.mock_calls), 2)
            self.assertEqual(
                argument_parser_mock.add_argument.mock_calls[0],
                (
                    ("--headless",),
                    {"action": "store_true", "help": "Run the application without GUI"},
                ),
            )
            self.assertEqual(
                argument_parser_mock.add_argument.mock_calls[1],
                (
                    ("--filename",),
                    {
                        "type": str,
                        "help": "File to ingest (only for mockup, not used in real application)", # noqa: E501
                    },
                ),
            )

    def test_returnsACLIArgumentsInstanceFromTheParsedArguments(self):
        """Returns a CLIArguments instance from the parsed arguments"""
        argparse_module_mock, argument_parser_mock, cli_arguments_module_mock = (
            set_up_mocks()
        )
        with patch.dict(
            "sys.modules",
            {
                "argparse": argparse_module_mock,
                "napytau.cli.cli_arguments": cli_arguments_module_mock,
            },
        ):
            from napytau.cli.parser import parse_cli_arguments

            test_args = Namespace(headless=True, filename="test_filename")
            argument_parser_mock.parse_args.return_value = test_args
            cli_arguments_module_mock.CLIArguments.return_value = MagicMock()
            parse_cli_arguments()
            self.assertEqual(
                cli_arguments_module_mock.CLIArguments.mock_calls[0], ((test_args,),)
            )


if __name__ == "__main__":
    unittest.main()
