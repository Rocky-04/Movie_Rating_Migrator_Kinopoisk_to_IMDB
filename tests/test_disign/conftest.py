import pytest
from PyQt5.QtWidgets import QMainWindow

from src.disign import UiMainWindow


@pytest.fixture()
def qtbot(qtbot, monkeypatch):
    """
    This fixture creates a `QMainWindow` object and an instance of the `UiMainWindow` class, and
    sets up the user interface for the main window. It also uses the `monkeypatch` fixture to
    temporarily replace the `print_massage` method of the `UiMainWindow` class with a dummy function
    that does nothing. This allows the tests to focus on the functionality being tested, without
    interference from the `print_massage` method.

    Parameters:
    qtbot (qtbot): A `qtbot` object for interacting with widgets during testing.
    monkeypatch (monkeypatch): A `monkeypatch` fixture for temporarily replacing the behavior of
    functions, methods, or attributes during testing.

    Returns:
    tuple: A tuple containing the `UiMainWindow` instance and the `QMainWindow` object.
    """
    # Create a main window and a virtual browser instance
    main_window = QMainWindow()
    ui = UiMainWindow()
    monkeypatch.setattr(UiMainWindow, "print_massage", lambda *args, **kwargs: None)

    # Add the main window to the qtbot fixture
    qtbot.addWidget(main_window)

    # Set up the user interface for the main window
    ui.setup_ui(main_window)

    return ui, main_window, qtbot


@pytest.fixture
def launch_for_test_massage():
    """
    Fixture for testing the `print_massage` method of the `UiMainWindow` class when the `side`
    argument is set to 'error'.
    Creates an instance of the `UiMainWindow` class, sets the `timer` attribute to 0, and calls
    the `print_massage` method with the argument 'This is an error message' and the keyword
    argument `side='error'`.
    Returns:
    UiMainWindow: An instance of the `UiMainWindow` class with the `timer` attribute set to 0 and
    the `print_massage` method called with the appropriate arguments.
    """
    ui = UiMainWindow()
    ui.timer = 0
    ui.print_massage('This is an error message', side='error')
    return ui