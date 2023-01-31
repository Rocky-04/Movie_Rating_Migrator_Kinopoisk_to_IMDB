import json
import os

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget

from src.browser import VirtualBrowser


class UiMainWindow(object):
    ICON_PATH = '../img/icon.ico'
    DEFAULT_PATH = '../data'

    def __init__(self):
        # Initialize instance variables
        self.user_id = None
        self.path_file = None
        self.timer = 60000  # 60 sec

    def setup_ui(self, main_window: QMainWindow) -> None:
        """
        Setup the user interface for the main window of the application.

        Parameters:
        main_window (QMainWindow): The main window object.
        """
        main_window.setObjectName("main_window")
        main_window.resize(481, 568)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(20)
        main_window.setFont(font)
        main_window.setMouseTracking(False)
        main_window.setStyleSheet("color: rgb(180, 142, 255);\n"
                                  "selection-background-color: rgb(221, 221, 221);")
        main_window.setWindowIcon(QtGui.QIcon(self.ICON_PATH))
        main_window.setIconSize(QtCore.QSize(100, 100))
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setStyleSheet("background-color: rgb(230, 230, 230);\n"
                                         "alternate-background-color: rgb(217, 215, 217);")
        self.centralwidget.setObjectName("centralwidget")
        main_window.setWindowTitle("Kinopoisk_IMDB")

        self.setup_label(self.centralwidget)
        self.setup_button_download(self.centralwidget)
        self.setup_button_rate(self.centralwidget)
        self.setup_button_send_path(self.centralwidget)
        self.setup_plain_text_edit(self.centralwidget)
        self.setup_button_enter_id(self.centralwidget)

        main_window.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(main_window)

        self.connect_slots()
        self.print_massage(
            'Для корректной работы понадобиться установленный браузер Google Chrome. <br> '
            'Также VPN если без него не работает Кинопоиск. <br><br>'
            'Если в програме не работает браузер, загрузите последнюю версию chromedriver для своей'
            ' системы <a href="https://chromedriver.chromium.org/downloads"> здесь. </a> '
            'Замените chromedriver в папке chrome_driver вашей загрузкой.')

    def setup_label(self, parent: QWidget) -> None:
        """
        Setup the label that displays a welcome message.

        Parameters:
        parent (QWidget): The parent widget for the label.
        """
        self.label_3 = QtWidgets.QLabel(parent)
        self.label_3.setGeometry(QtCore.QRect(20, 10, 450, 121))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setStyleSheet("color: rgb(11, 11, 11);\n"
                                   "background-color: rgb(231, 231, 231);")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        text = ("<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">Укажите ID "
                "пользователя Кинопоиск у которого </span></p><p align=\"center\"><span style=\" "
                "font-size:9pt;\">нужно скачать оценки.</span></p><p align=\"center\"><span style="
                "\" font-size:9pt;\">Узнать ID вы можете во вкладке оценки</span></p><p align=\""
                "center\"><span style=\" font-size:9pt;\"><br/></span></p></body></html>")
        self.label_3.setText(text)

    def setup_button_download(self, parent: QWidget) -> None:
        """
        Setup the button for downloading ratings.

        Parameters:
        parent (QWidget): The parent widget for the button.
        """
        self.button_download = QtWidgets.QPushButton(parent)
        self.button_download.setGeometry(QtCore.QRect(20, 380, 450, 80))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(15)
        self.button_download.setFont(font)
        self.button_download.setStyleSheet("color: rgb(3, 3, 3);\n"
                                           "background-color: rgb(221, 221, 221);")
        self.button_download.setObjectName("button_download")
        self.button_download.setText("Скачать оценки Кинопоиск в Excel")

    def setup_button_rate(self, parent: QWidget) -> None:
        """
        Setup the button for uploading ratings.

        Parameters:
        parent (QWidget): The parent widget for the button.
        """
        self.button_rate = QtWidgets.QPushButton(parent)
        self.button_rate.setGeometry(QtCore.QRect(20, 470, 450, 80))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(15)
        self.button_rate.setFont(font)
        self.button_rate.setStyleSheet("color: rgb(0, 0, 0);\n"
                                       "background-color: rgb(202, 202, 202);")
        self.button_rate.setText("Скачать оценки с Кинопоиск \n"
                                 "и проставить IMDB")
        self.button_rate.setAutoRepeat(False)
        self.button_rate.setAutoExclusive(False)
        self.button_rate.setAutoDefault(False)
        self.button_rate.setDefault(False)
        self.button_rate.setObjectName("button_rate")

    def setup_button_send_path(self, central_widget: QWidget) -> None:
        """
        Setup the send path button.

        Parameters:
        central_widget (QWidget): The central widget object.
        """
        self.button_send_path = QtWidgets.QPushButton(central_widget)
        self.button_send_path.setGeometry(QtCore.QRect(20, 290, 450, 80))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.button_send_path.setFont(font)
        self.button_send_path.setStyleSheet("background-color: rgb(255, 99, 85);\n"
                                            "color: rgb(0, 0, 0);\n"
                                            "\n"
                                            "")
        self.button_send_path.setObjectName("button_send_path")
        self.button_send_path.setText("Укажите путь для сохранения файла:")

    def setup_button_enter_id(self, central_widget: QWidget) -> None:
        """
        Setup the enter ID button.

        Parameters:
        central_widget (QWidget): The central widget object.
        """
        self.button_enter_id = QtWidgets.QPushButton(self.centralwidget)
        self.button_enter_id.setGeometry(QtCore.QRect(20, 200, 450, 80))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.button_enter_id.setFont(font)
        self.button_enter_id.setStyleSheet("background-color: rgb(255, 99, 85);\n"
                                           "color: rgb(0, 0, 0);\n"
                                           "\n"
                                           "")
        self.button_enter_id.setObjectName("button_enter_id")
        self.button_enter_id.setText("Нажмите когда укажите ID")

    def setup_plain_text_edit(self, central_widget: QWidget) -> None:
        """
        Setup the plain text edit widget.

        Parameters:
        central_widget (QWidget): The central widget object.
        """
        self.plain_text_edit = QtWidgets.QPlainTextEdit(central_widget)
        self.plain_text_edit.setGeometry(QtCore.QRect(20, 150, 450, 40))
        self.plain_text_edit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                           "color: rgb(2, 2, 2);\n"
                                           "font: 12pt;\n"
                                           "")
        self.plain_text_edit.setObjectName("plain_text_edit")

    def print_massage(self, text: str, side: str = 'massage') -> None:
        """
        Displays a message to the user.
        A timer is used to close the message box after a certain period of time.

        text (str): The message to be displayed.
        message_type (str, optional): The type of message. Can be 'message' or 'error'.
                Defaults to 'message'.
        """
        massage = QMessageBox()
        if side == 'error':
            massage.setWindowTitle('Error')
            massage.setIcon(QMessageBox.Warning)
        else:
            massage.setWindowTitle('Important')
            massage.setIcon(QMessageBox.Information)
        massage.setText(text)
        massage.setStandardButtons(QMessageBox.Ok)
        massage.setWindowIcon(QtGui.QIcon(self.ICON_PATH))
        timer = QTimer(massage)
        timer.setInterval(self.timer)
        timer.setSingleShot(True)
        timer.timeout.connect(massage.accept)
        timer.start()
        massage.exec_()
        self.massage = massage

    def connect_slots(self) -> None:
        """
        Connect the signals and slots of the user interface.
        """
        self.button_download.clicked.connect(self.parse_user_ratings)
        self.button_enter_id.clicked.connect(self.send_user_id)
        self.button_send_path.clicked.connect(self.select_save_path)
        self.button_rate.clicked.connect(self.rate_movies_on_imdb)

    def send_user_id(self) -> None:
        """
        Transmits the KinoPoisk ID.

        Verifies that the user-entered ID is a valid ID, i.e. it consists only of digits
        and has a length of 2 to 20 characters. If the ID is valid, sets it to the
        self.user_id variable and changes the color of the button_enter_id button.
        Otherwise, displays an error message using the self.print_massage function.
        """
        user_input = self.plain_text_edit.toPlainText()
        min_length = 2
        max_length = 15
        error_message = (
            f"Некоректный ID, он должен состоять только из цифр "
            f"и иметь длину от {min_length} до {max_length} символов"
        )

        if not user_input:
            self.print_massage(text="Введите ID", side="error")
            return

        if not user_input.isnumeric():
            self.print_massage(text=error_message, side="error")
            return
        try:
            if min_length <= len(user_input) <= max_length and user_input[0] != '0':
                self.user_id = int(user_input)
                self.button_enter_id.setStyleSheet("background-color: rgb(80, 255, 115);\n"
                                                   "color: rgb(0, 0, 0);\n")
            else:
                self.print_massage(text=error_message, side="error")
        except Exception as error:
            print(error)
            self.print_massage(text=error_message, side="error")

    def select_save_path(self) -> None:
        """
        Transmits the path for saving files.

        Opens a file dialog to allow the user to select a directory for saving files.
        Removes the trailing '/' from the selected path if it exists.
        If a path is selected, changes the color of the button_send_path button.
        """
        path = QFileDialog.getExistingDirectory(directory=self.DEFAULT_PATH)
        if len(path) > 0 and not path.isdigit():
            self.button_send_path.setStyleSheet("background-color: rgb(80, 255, 115);\n"
                                                "color: rgb(0, 0, 0);\n")
        else:
            self.print_massage('Не выбран путь для сохранения файла')
            return
        if path.endswith('/'):
            path = path[0:-1]
        self.path_file = path

    def parse_user_ratings(self) -> None:
        """
        Parses KinoPoisk.

        Verifies that the user ID and save path are set. If either is not set,
        displays an error message using the self.print_message function.
        Otherwise, starts parsing using the VirtualBrowser class. If the parsing is successful,
        displays a success message using the self.print_message function.
        If the parsing fails, displays an error message with troubleshooting tips using the
        self.print_message function.
        """
        user_id = self.user_id
        path_file = self.path_file
        if not user_id or not path_file:
            text = "Не указан путь для сохранения или ID"
            self.print_massage(text=text, side='error')
            return

        text = ('Для парсинга Ваших оценок с Кинопоиска, возможно понадобиться пройти '
                'проверку на то что вы человек. Не закрывайте открытый браузер программой!')
        self.print_massage(text)
        for _ in range(3):
            try:
                self.browser = VirtualBrowser(user_id, path_file).parse_user_ratings()
                text = f'''Парсинг успешно завершен. Файлы сохранены в папку {path_file}'''
                self.print_massage(text)
                return
            except Exception as e:
                print(e)
                continue

        text = ("Произошла ошибка при парсинге данных.<br><br>"
                "Проверьте открываться ли у Вас сайт Кинопоиска, возможно нужен VPN.<br>"
                "Проверьте правильность ID пользователя.<br>"
                "Проверьте драйвера браузера, загрузите последнюю версию chromedriver для "
                "своей системы <a href='https://chromedriver.chromium.org/downloads'>здесь."
                " </a> Замените chromedriver в папке chrome_driver вашей загрузкой.<br>"
                )
        self.print_massage(text=text, side='error')

    def rate_movies_on_imdb(self) -> None:
        """
        Rates movies on IMDB. If a rating_data.json file exists, a pop-up window will appear asking
        the user if they want to continue rating movies or start parsing again. If the file does not
        exist, parsing will start immediately. If an error occurs during the rating process, it will
        be caught and a message will be printed.
        """
        user_id = self.user_id
        path_file = self.path_file

        if not path_file:
            text = "Не указан путь для сохранения"
            self.print_massage(text=text, side='error')
            return

        # Check if rating_data.json file exists
        path = str(path_file) + '/rating_data.json'
        if os.path.exists(path):
            # If file exists, open it and count the number of ratings
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                rating_count = len(data)

            self.show_rating_popup(rating_count)

        elif not user_id:
            text = "Не указан ID пользователя"
            self.print_massage(text=text, side='error')
            return
        else:
            self.parse_user_ratings()

        text = ("Для проставления оценок на Ваш IMDB, понадобиться пройти авторизацию на сайте."
                " Сам процесс занимает время, так как каждый фильм проставляется отдельно. "
                "В среднем на один фильм уходит 3 сек, 1000 оценок займет около 50 мин:-)")
        self.print_massage(text)

        try:
            self.browser = VirtualBrowser(user_id, path_file).start_rate_imdb()

            text = f"""Файл с ошибками (если они были) сохранен в папку {path_file}"""
            self.print_massage(text)

        except Exception as e:
            print(e)
            text = ("Произошла ошибка при проставлении оценок. Попробуйте позже, если опять"
                    " будет ошибка напишите в тех. поддержку - rocky01396@gmail.com")
            self.print_massage(text=text, side='error')

    def show_rating_popup(self, rating_count: int) -> None:
        """
        Shows a pop-up window to the user, asking if they want to continue rating movies using an
        existing rating_data.json file or start parsing again. The number of ratings in the file is
        passed as an argument.

        :param rating_count: The number of ratings.
        """

        def handle_popup_response(answer) -> None:
            """
            Handles the user's response to the pop-up window by either starting parsing again or
            continuing with the rating process.
            """
            if 'No' in answer.text():
                self.parse_user_ratings()

        massage = QMessageBox()
        massage.setWindowTitle('Important')
        text = f'Найден файл с оценками, в котором {rating_count} оценок. ' + (
            "Если вы уже начинали проставлять оценки, они продолжат проставляться с места "
            "последней остановки. Желаете использовать этот файл? Если ответите NO, "
            "оценки будут скачаны заново с Кинопоиск и проставляться тоже будут заново")
        massage.setText(text)
        massage.setIcon(QMessageBox.Question)
        massage.setWindowIcon(QtGui.QIcon(self.ICON_PATH))
        massage.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        massage.buttonClicked.connect(handle_popup_response)
        massage.exec_()
