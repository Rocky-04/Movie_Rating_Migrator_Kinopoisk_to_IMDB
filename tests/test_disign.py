import pytest
from PyQt5 import QtWidgets
from pytestqt import qtbot
from src.disign import UiMainWindow

def test_setup_label(qtbot):
    # Create a dummy parent widget and a label
    parent = QtWidgets.QWidget()
    label = QtWidgets.QLabel(parent)

    # Call the setup_label method with the label and the parent widget as arguments
    UiMainWindow.setup_label(label, parent)

    # Assert that the label has been added to the parent widget's layout
    assert label in parent.layout().items()


def test_ui_main_window(qtbot):
    # Create a main window object
    main_window = QtWidgets.QMainWindow()

    # Create an instance of the UiMainWindow class
    ui_main_window = UiMainWindow()

    # Call the setup_ui method with the main window object as an argument
    ui_main_window.setup_ui(main_window)

    # Assert that the main window object has a central widget
    assert main_window.centralWidget() is not None