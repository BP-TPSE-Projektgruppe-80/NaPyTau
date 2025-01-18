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
            self.assertEqual(len(argument_parser_mock.add_argument.mock_calls), 5)
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
                    ("--dataset_format",),
                    {
                        "type": str,
                        "default": "legacy",
                        "const": "legacy",
                        "nargs": "?",
                        "choices": ["legacy", "napytau"],
                        "help": "Format of the dataset to ingest",
                    },
                ),
            )

            self.assertEqual(
                argument_parser_mock.add_argument.mock_calls[2],
                (
                    ("--data_files_directory",),
                    {
                        "type": str,
                        "help": """Path to the directory containing either data files or subdirectories
        with data files""",
                    },
                ),
            )

            self.assertEqual(
                argument_parser_mock.add_argument.mock_calls[3],
                (
                    ("--fit_file",),
                    {
                        "type": str,
                        "help": """Path to a fit file to use instead of the one found in the setup files,
        only relevant for legacy format"""
                    },
                ),
            )

            self.assertEqual(
                argument_parser_mock.add_argument.mock_calls[4],
                (
                    ("--setup_identifier",),
                    {
                        "type": str,
                        "help": """Identifier of the setup to use with the dataset, file path for legacy
        format, or setup name for NaPyTau format""",
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

            test_args = Namespace(
                headless=True,
                dataset_format="legacy",
                setup_files_directory="test_directory",
                fit_file="test_file",
            )
            argument_parser_mock.parse_args.return_value = test_args
            cli_arguments_module_mock.CLIArguments.return_value = MagicMock()
            parse_cli_arguments()
            self.assertEqual(
                cli_arguments_module_mock.CLIArguments.mock_calls[0], ((test_args,),)
            )


if __name__ == "__main__":
    unittest.main()
