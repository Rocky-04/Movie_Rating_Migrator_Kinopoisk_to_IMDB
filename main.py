from PyQt5 import QtWidgets

from src.disign import UiMainWindow


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(main_window)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
