import pytest
from PyQt5.QtWidgets import QMainWindow
from src.disign import UiMainWindow

@pytest.fixture(autouse=True)
def create_main_window():
    # Create a main window and a virtual browser instance
    main_window = QMainWindow()
    ui = UiMainWindow()
