import unittest
from argparse import Namespace
from unittest.mock import MagicMock, patch


def set_up_mocks() -> (MagicMock, MagicMock, MagicMock):
    parser_mock = MagicMock()
    gui_mock = MagicMock()
    headless_mock = MagicMock()
    return parser_mock, gui_mock, headless_mock


class MainUnitTest(unittest.TestCase):
    def test_callsTheHeadlessInitFunctionIfTheHeadlessFlagIsSupplied(self) -> None:
        """Calls the headless init function if the headless flag is supplied"""
        parser_mock, gui_mock, headless_mock = set_up_mocks()
        with patch.dict(
            "sys.modules",
            {
                "gui.ui_mockup": gui_mock,
                "headless.headless_mockup": headless_mock,
                "cli.parser": parser_mock,
            },
        ):
            headless_mock.init = MagicMock()
            parser_mock.parse_cli_arguments.return_value = Namespace(
                headless=True, filename=None
            )

            from napytau.main import main

            main()
            self.assertEqual(len(headless_mock.init.mock_calls), 1)

    def test_callsTheGuiInitFunctionIfTheHeadlessFlagIsNotSupplied(self) -> None:
        """Calls the GUI init function if the headless flag is not supplied"""
        parser_mock, gui_mock, headless_mock = set_up_mocks()
        with patch.dict(
            "sys.modules",
            {
                "gui.ui_mockup": gui_mock,
                "headless.headless_mockup": headless_mock,
                "cli.parser": parser_mock,
            },
        ):
            gui_mock.init = MagicMock()
            parser_mock.parse_cli_arguments.return_value = Namespace(
                headless=False, filename=None
            )

            from napytau.main import main

            main()
            self.assertEqual(len(gui_mock.init.mock_calls), 1)


if __name__ == "__main__":
    unittest.main()
