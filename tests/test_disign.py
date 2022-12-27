import pytest
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

from src.browser import VirtualBrowser


def test_setup_ui_sets_window_size(qtbot):
    ui, main_window, qtbot = qtbot
    assert main_window.size() == QtCore.QSize(481, 568)


def test_setup_ui_sets_window_font(qtbot):
    ui, main_window, qtbot = qtbot
    assert main_window.font().family() == "Yu Gothic UI"
    assert main_window.font().pointSize() == 20


def test_setup_ui_sets_window_style(qtbot):
    ui, main_window, qtbot = qtbot
    assert main_window.styleSheet() == ("color: rgb(180, 142, 255);\nselection-background-color: "
                                        "rgb(221, 221, 221);")


def test_setup_ui_sets_window_icon(qtbot):
    ui, main_window, qtbot = qtbot
    assert main_window.windowIcon().isNull() is False
    assert main_window.iconSize() == QtCore.QSize(100, 100)


def test_setup_ui_sets_window_title(qtbot):
    ui, main_window, qtbot = qtbot
    assert main_window.windowTitle() == "Kinopoisk_IMDB"


def test_setup_ui_sets_central_widget(qtbot):
    ui, main_window, qtbot = qtbot
    assert main_window.centralWidget() == ui.centralwidget


def test_setup_label_creates_label_with_correct_parent(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.label_3.parent() == ui.centralwidget


def test_setup_label_sets_label_geometry(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.label_3.geometry() == QtCore.QRect(20, 10, 450, 121)


def test_setup_label_sets_label_font(qtbot):
    ui, main_window, qtbot = qtbot
    font = QtGui.QFont()
    font.setFamily("Yu Gothic UI")
    font.setPointSize(10)
    font.setWeight(75)
    assert ui.label_3.font().family() == font.family()
    assert ui.label_3.font().pointSize() == font.pointSize()
    assert ui.label_3.font().weight() == font.weight()


def test_setup_label_sets_label_layout_direction(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.label_3.layoutDirection() == QtCore.Qt.LeftToRight


def test_setup_label_sets_label_style_sheet(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.label_3.styleSheet() == ("color: rgb(11, 11, 11);\nbackground-color: "
                                       "rgb(231, 231, 231);")


def test_setup_label_sets_label_alignment(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.label_3.alignment() == QtCore.Qt.AlignCenter


def test_setup_label_sets_text(qtbot):
    ui, main_window, qtbot = qtbot
    expected_text = (
        "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">Укажите ID "
        "пользователя Кинопоиск у которого </span></p><p align=\"center\"><span style=\" "
        "font-size:9pt;\">нужно скачать оценки.</span></p><p align=\"center\"><span style="
        "\" font-size:9pt;\">Узнать ID вы можете во вкладке оценки</span></p><p align=\""
        "center\"><span style=\" font-size:9pt;\"><br/></span></p></body></html>")
    assert ui.label_3.text() == expected_text


def test_setup_button_download_creates_button_with_correct_parent(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_download.parent() == ui.centralwidget


def test_setup_button_download_sets_button_geometry(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_download.geometry() == QtCore.QRect(20, 380, 450, 80)


def test_setup_button_download_sets_button_font(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_download.font().family() == "Yu Gothic UI"
    assert ui.button_download.font().pointSize() == 15


def test_setup_button_download_sets_button_style(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_download.styleSheet() == ("color: rgb(3, 3, 3);\nbackground-color: "
                                               "rgb(221, 221, 221);")


def test_setup_button_download_sets_button_text(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_download.text() == "Скачать оценки Кинопоиск в Excel"


def test_setup_button_rate_creates_button_with_correct_parent(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_rate.parent() == ui.centralwidget


def test_setup_button_rate_sets_button_geometry(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_rate.geometry() == QtCore.QRect(20, 470, 450, 80)


def test_setup_button_rate_sets_button_font(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_rate.font().family() == "Yu Gothic UI"
    assert ui.button_rate.font().pointSize() == 15


def test_setup_button_rate_sets_button_stylesheet(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_rate.styleSheet() == ("color: rgb(0, 0, 0);\nbackground-color:"
                                           " rgb(202, 202, 202);")


def test_setup_button_rate_sets_button_text(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_rate.text() == "Скачать оценки с Кинопоиск \nи проставить IMDB"


def test_setup_button_rate_sets_auto_repeat_to_false(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_rate.autoRepeat() is False


def test_setup_button_rate_sets_auto_exclusive_to_false(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_rate.autoExclusive() is False


def test_setup_button_rate_sets_auto_default_to_false(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_rate.autoDefault() is False


def test_setup_button_rate_sets_default_to_false(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_rate.isDefault() is False


def test_setup_button_send_path_creates_button_with_correct_parent(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_send_path.parent() == ui.centralwidget


def test_setup_button_send_path_sets_button_geometry(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_send_path.geometry() == QtCore.QRect(20, 290, 450, 80)


def test_setup_button_send_path_sets_button_font(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_send_path.font().family() == "Segoe UI"
    assert ui.button_send_path.font().pointSize() == 15


def test_setup_button_send_path_sets_button_style(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_send_path.styleSheet() == ('background-color: rgb(255, 99, 85);\ncolor: '
                                                'rgb(0, 0, 0);\n\n')


def test_setup_button_send_path_sets_button_text(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_send_path.text() == "Укажите путь для сохранения файла:"


def test_setup_plain_text_edit_creates_plain_text_edit_with_correct_parent(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.plain_text_edit.parent() == ui.centralwidget


def test_setup_plain_text_edit_sets_plain_text_edit_geometry(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.plain_text_edit.geometry() == QtCore.QRect(20, 150, 450, 40)


def test_setup_plain_text_edit_sets_plain_text_edit_style_sheet(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.plain_text_edit.styleSheet() == ("background-color: rgb(255, 255, 255);\n"
                                               "color: rgb(2, 2, 2);\n"
                                               "font: 12pt;\n")


def test_setup_plain_text_edit_sets_plain_text_edit_object_name(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.plain_text_edit.objectName() == "plain_text_edit"


def test_setup_button_download_has_correct_parent(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_download.parent() == ui.centralwidget


def test_setup_button_download_has_correct_geometry(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_download.geometry() == QtCore.QRect(20, 380, 450, 80)


def test_setup_button_download_has_correct_font(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_download.font().family() == "Yu Gothic UI"
    assert ui.button_download.font().pointSize() == 15


def test_setup_button_download_has_correct_style_sheet(qtbot):
    ui, main_window, qtbot = qtbot
    assert ui.button_download.styleSheet() == ('color: rgb(3, 3, 3);\nbackground-color: '
                                               'rgb(221, 221, 221);')


def test_print_massage_sets_window_title_correctly_on_error(launch_for_test_massage):
    ui = launch_for_test_massage
    assert ui.massage.windowTitle() == 'Error'


def test_print_massage_sets_icon_correctly_on_error(launch_for_test_massage):
    ui = launch_for_test_massage
    assert ui.massage.icon() == QMessageBox.Warning


def test_print_massage_sets_text_correctly(launch_for_test_massage):
    ui = launch_for_test_massage
    assert ui.massage.text() == 'This is an error message'


def test_print_massage_sets_standard_buttons_correctly(launch_for_test_massage):
    ui = launch_for_test_massage
    assert ui.massage.standardButtons() == QMessageBox.Ok


def test_connect_button_download(qtbot):
    ui, main_window, qtbot = qtbot
    function_call_count = 0

    def count_function_calls():
        """function that increments the counter variable each time it is called"""
        nonlocal function_call_count
        function_call_count += 1

    # Connect the count_function_calls function to the clicked signal of the button
    ui.button_download.clicked.connect(count_function_calls)

    # Simulate a mouse click on the button
    qtbot.mouseClick(ui.button_download, QtCore.Qt.LeftButton)

    assert function_call_count == 1


def test_connect_button_rate(qtbot):
    ui, main_window, qtbot = qtbot
    function_call_count = 0

    def count_function_calls():
        """Function that increments the counter variable each time it is called."""
        nonlocal function_call_count
        function_call_count += 1

    ui.button_rate.clicked.connect(count_function_calls)
    qtbot.mouseClick(ui.button_rate, QtCore.Qt.LeftButton)

    assert function_call_count == 1


def test_connect_button_enter_id(qtbot):
    ui, main_window, qtbot = qtbot
    function_call_count = 0

    def count_function_calls():
        """Function that increments the counter variable each time it is called."""
        nonlocal function_call_count
        function_call_count += 1

    ui.button_enter_id.clicked.connect(count_function_calls)
    qtbot.mouseClick(ui.button_enter_id, QtCore.Qt.LeftButton)

    assert function_call_count == 1


@pytest.mark.parametrize('user_id, result', [
    (252, True),
    ('fs', False),
    (1, False),
    ('000', False),
    ('545421sf5454', False),
    (4545124541245114, False),
    ('054515', False)
])
def test_send_user_id(qtbot, monkeypatch, user_id, result):
    ui, main_window, qtbot = qtbot
    monkeypatch.setattr(ui.plain_text_edit, "toPlainText", lambda *args, **kwargs: str(user_id))

    qtbot.mouseClick(ui.button_enter_id, QtCore.Qt.LeftButton)
    if result:
        assert ui.user_id == user_id
    else:
        assert ui.user_id is None


@pytest.mark.parametrize('path_file, result', [
    ('0', False),
    ('fs', True),
    (1, False),
    ('000', False),
    ('545421sf5454', True),
    ('', False),
])
def test_select_save_path(qtbot, monkeypatch, path_file, result):
    ui, main_window, qtbot = qtbot
    monkeypatch.setattr(QFileDialog, "getExistingDirectory", lambda *args, **kwargs: str(path_file))

    qtbot.mouseClick(ui.button_send_path, QtCore.Qt.LeftButton)
    if result:
        assert ui.path_file == path_file
    else:
        assert ui.path_file is None


@pytest.mark.parametrize('user_id, path_file, result', [
    ('555', '', False),
    ('', 'path', False),
    ('5555', 'path', True),
])
def test_start_parsing(qtbot, monkeypatch, path_file, user_id, result):
    ui, main_window, qtbot = qtbot
    monkeypatch.setattr(VirtualBrowser, "start_parsing", lambda *args, **kwargs: result)

    ui.path_file = path_file
    ui.user_id = user_id

    qtbot.mouseClick(ui.button_download, QtCore.Qt.LeftButton)

    assert hasattr(ui, 'browser') == result


@pytest.mark.parametrize('user_id, path_file, result', [
    ('555', '', False),
    ('', 'path', False),
    ('5555', 'path', True),
])
def test_rate_movies_on_imdb(qtbot, monkeypatch, path_file, user_id, result):
    ui, main_window, qtbot = qtbot
    monkeypatch.setattr(VirtualBrowser, "start_rate_imdb", lambda *args, **kwargs: result)
    monkeypatch.setattr(VirtualBrowser, "start_parsing", lambda *args, **kwargs: result)

    ui.path_file = path_file
    ui.user_id = user_id

    qtbot.mouseClick(ui.button_rate, QtCore.Qt.LeftButton)
    print(hasattr(ui, 'browser'))
    assert hasattr(ui, 'browser') == result
