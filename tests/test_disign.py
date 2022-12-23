from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

from src.disign import UiMainWindow


def create_main_window(qtbot, monkeypatch):
    # Create a main window and a virtual browser instance
    main_window = QMainWindow()
    ui = UiMainWindow()
    monkeypatch.setattr(UiMainWindow, "print_massage", lambda *args, **kwargs: None)

    # Add the main window to the qtbot fixture
    qtbot.addWidget(main_window)

    # Set up the user interface for the main window
    ui.setup_ui(main_window)

    return ui, main_window


def test_setup_ui_sets_window_size(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert main_window.size() == QtCore.QSize(481, 568)


def test_setup_ui_sets_window_font(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert main_window.font().family() == "Yu Gothic UI"
    assert main_window.font().pointSize() == 20


def test_setup_ui_sets_window_style(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert main_window.styleSheet() == ("color: rgb(180, 142, 255);\nselection-background-color: "
                                        "rgb(221, 221, 221);")


def test_setup_ui_sets_window_icon(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert main_window.windowIcon().isNull() is False
    assert main_window.iconSize() == QtCore.QSize(100, 100)


def test_setup_ui_sets_window_title(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert main_window.windowTitle() == "Kinopoisk_IMDB"


def test_setup_ui_sets_central_widget(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert main_window.centralWidget() == ui.centralwidget


def test_setup_label_creates_label_with_correct_parent(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.label_3.parent() == ui.centralwidget


def test_setup_label_sets_label_geometry(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.label_3.geometry() == QtCore.QRect(20, 10, 450, 121)


def test_setup_label_sets_label_font(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    font = QtGui.QFont()
    font.setFamily("Yu Gothic UI")
    font.setPointSize(10)
    font.setWeight(75)
    assert ui.label_3.font().family() == font.family()
    assert ui.label_3.font().pointSize() == font.pointSize()
    assert ui.label_3.font().weight() == font.weight()


def test_setup_label_sets_label_layout_direction(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.label_3.layoutDirection() == QtCore.Qt.LeftToRight


def test_setup_label_sets_label_style_sheet(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.label_3.styleSheet() == ("color: rgb(11, 11, 11);\nbackground-color: "
                                       "rgb(231, 231, 231);")


def test_setup_label_sets_label_alignment(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.label_3.alignment() == QtCore.Qt.AlignCenter


def test_setup_label_sets_text(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    expected_text = (
        "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">Укажите ID "
        "пользователя Кинопоиск у которого </span></p><p align=\"center\"><span style=\" "
        "font-size:9pt;\">нужно скачать оценки.</span></p><p align=\"center\"><span style="
        "\" font-size:9pt;\">Узнать ID вы можете во вкладке оценки</span></p><p align=\""
        "center\"><span style=\" font-size:9pt;\"><br/></span></p></body></html>")
    assert ui.label_3.text() == expected_text


def test_setup_button_download_creates_button_with_correct_parent(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_download.parent() == ui.centralwidget


def test_setup_button_download_sets_button_geometry(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_download.geometry() == QtCore.QRect(20, 380, 450, 80)


def test_setup_button_download_sets_button_font(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_download.font().family() == "Yu Gothic UI"
    assert ui.button_download.font().pointSize() == 15


def test_setup_button_download_sets_button_style(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_download.styleSheet() == ("color: rgb(3, 3, 3);\nbackground-color: "
                                               "rgb(221, 221, 221);")


def test_setup_button_download_sets_button_text(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_download.text() == "Скачать оценки Кинопоиск в Excel"


def test_setup_button_rate_creates_button_with_correct_parent(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_rate.parent() == ui.centralwidget


def test_setup_button_rate_sets_button_geometry(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_rate.geometry() == QtCore.QRect(20, 470, 450, 80)


def test_setup_button_rate_sets_button_font(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_rate.font().family() == "Yu Gothic UI"
    assert ui.button_rate.font().pointSize() == 15


def test_setup_button_rate_sets_button_stylesheet(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_rate.styleSheet() == ("color: rgb(0, 0, 0);\nbackground-color:"
                                           " rgb(202, 202, 202);")


def test_setup_button_rate_sets_button_text(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_rate.text() == "Скачать оценки с Кинопоиск \nи проставить IMDB"


def test_setup_button_rate_sets_auto_repeat_to_false(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_rate.autoRepeat() is False


def test_setup_button_rate_sets_auto_exclusive_to_false(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_rate.autoExclusive() is False


def test_setup_button_rate_sets_auto_default_to_false(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_rate.autoDefault() is False


def test_setup_button_rate_sets_default_to_false(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_rate.isDefault() is False


def test_setup_button_send_path_creates_button_with_correct_parent(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_send_path.parent() == ui.centralwidget


def test_setup_button_send_path_sets_button_geometry(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_send_path.geometry() == QtCore.QRect(20, 290, 450, 80)


def test_setup_button_send_path_sets_button_font(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_send_path.font().family() == "Segoe UI"
    assert ui.button_send_path.font().pointSize() == 15


def test_setup_button_send_path_sets_button_style(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_send_path.styleSheet() == ('background-color: rgb(255, 99, 85);\ncolor: '
                                                'rgb(0, 0, 0);\n\n')


def test_setup_button_send_path_sets_button_text(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_send_path.text() == "Укажите путь для сохранения файла:"


def test_setup_plain_text_edit_creates_plain_text_edit_with_correct_parent(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.plain_text_edit.parent() == ui.centralwidget


def test_setup_plain_text_edit_sets_plain_text_edit_geometry(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.plain_text_edit.geometry() == QtCore.QRect(20, 150, 450, 40)


def test_setup_plain_text_edit_sets_plain_text_edit_style_sheet(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.plain_text_edit.styleSheet() == ("background-color: rgb(255, 255, 255);\n"
                                               "color: rgb(2, 2, 2);\n"
                                               "font: 12pt;\n")


def test_setup_plain_text_edit_sets_plain_text_edit_object_name(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.plain_text_edit.objectName() == "plain_text_edit"


def test_setup_button_download_has_correct_parent(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_download.parent() == ui.centralwidget


def test_setup_button_download_has_correct_geometry(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_download.geometry() == QtCore.QRect(20, 380, 450, 80)


def test_setup_button_download_has_correct_font(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_download.font().family() == "Yu Gothic UI"
    assert ui.button_download.font().pointSize() == 15


def test_setup_button_download_has_correct_style_sheet(qtbot, monkeypatch):
    ui, main_window = create_main_window(qtbot, monkeypatch)
    assert ui.button_download.styleSheet() == ('color: rgb(3, 3, 3);\nbackground-color: '
                                               'rgb(221, 221, 221);')


def create_main_window_for_test_massage(qtbot):
    ui = UiMainWindow()
    ui.timer = 0
    ui.print_massage('This is an error message', side='error')
    return ui


def test_print_massage_sets_window_title_correctly_on_error(qtbot):
    ui = create_main_window_for_test_massage(qtbot)
    assert ui.massage.windowTitle() == 'Error'


def test_print_massage_sets_icon_correctly_on_error(qtbot):
    ui = create_main_window_for_test_massage(qtbot)
    assert ui.massage.icon() == QMessageBox.Warning


def test_print_massage_sets_text_correctly(qtbot):
    ui = create_main_window_for_test_massage(qtbot)
    assert ui.massage.text() == 'This is an error message'


def test_print_massage_sets_standard_buttons_correctly(qtbot):
    ui = create_main_window_for_test_massage(qtbot)
    assert ui.massage.standardButtons() == QMessageBox.Ok
