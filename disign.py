import json

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

from VirtualBrowser import VirtualBrowser


class Ui_MainWindow(object):
    user_id, path_file = None, None

    def setupUi(self, MainWindow):
        """Интерфейс приложения"""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(481, 568)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(20)
        MainWindow.setFont(font)
        MainWindow.setMouseTracking(False)
        MainWindow.setStyleSheet("color: rgb(180, 142, 255);\n"
                                 "selection-background-color: rgb(221, 221, 221);")
        MainWindow.setWindowIcon(QtGui.QIcon('icon.ico'))
        MainWindow.setIconSize(QtCore.QSize(100, 100))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(230, 230, 230);\n"
                                         "alternate-background-color: rgb(217, 215, 217);")
        self.centralwidget.setObjectName("centralwidget")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
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
        self.button_download = QtWidgets.QPushButton(self.centralwidget)
        self.button_download.setGeometry(QtCore.QRect(20, 380, 450, 80))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(15)
        self.button_download.setFont(font)
        self.button_download.setStyleSheet("color: rgb(3, 3, 3);\n"
                                           "background-color: rgb(221, 221, 221);")
        self.button_download.setObjectName("button_download")
        self.button_rate = QtWidgets.QPushButton(self.centralwidget)
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
        self.button_send_path = QtWidgets.QPushButton(self.centralwidget)
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
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 150, 450, 40))
        self.plainTextEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                         "color: rgb(2, 2, 2);\n"
                                         "font: 12pt;\n"
                                         "")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.button_send_path_2 = QtWidgets.QPushButton(self.centralwidget)
        self.button_send_path_2.setGeometry(QtCore.QRect(20, 200, 450, 80))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        self.button_send_path_2.setFont(font)
        self.button_send_path_2.setStyleSheet("background-color: rgb(255, 99, 85);\n"
                                              "color: rgb(0, 0, 0);\n"
                                              "\n"
                                              "")
        self.button_send_path_2.setObjectName("button_send_path_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.add_func()
        self.print_massage(
            'Для корректной работы понадобиться установленный браузер Google Chrome версии 104, а также VPN если без него не работает Кинопоиск')

    def print_massage(self, text, side='massage'):
        """
        Выводит текст пользователю.
        side = 'massage' or 'error'
        """
        massage = QMessageBox()
        if side == 'error':
            massage.setWindowTitle('Ошибка')
            massage.setIcon(QMessageBox.Warning)
        else:
            massage.setWindowTitle('Важно!')
            massage.setIcon(QMessageBox.Information)
        massage.setText(text)
        massage.setStandardButtons(QMessageBox.Ok)
        massage.setWindowIcon(QtGui.QIcon('icon.ico'))
        massage.exec_()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Kinopoisk_IMDB"))
        self.label_3.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">Укажите ID пользователя Кинопоиск у которого </span></p><p align=\"center\"><span style=\" font-size:9pt;\">нужно скачать оценки.</span></p><p align=\"center\"><span style=\" font-size:9pt;\">Узнать ID вы можете во вкладке оценки</span></p><p align=\"center\"><span style=\" font-size:9pt;\"><br/></span></p></body></html>"))
        self.button_download.setText(_translate("MainWindow", "Скачать оценки с Кинопоиск в Excel"))
        self.button_send_path.setText(_translate("MainWindow", "Укажите путь для сохранения файла:"))
        self.button_send_path_2.setText(_translate("MainWindow", "Нажмите когда укажите ID"))

    def add_func(self):
        """Реагирует на нажатия кнопок"""
        self.button_download.clicked.connect(lambda: self.func_start_download(self.user_id, self.path_file))
        self.button_send_path_2.clicked.connect(lambda: self.func_send_id())
        self.button_send_path.clicked.connect(lambda: self.func_send_path())
        self.button_rate.clicked.connect(lambda: self.func_start_rate(self.user_id, self.path_file))

    def func_send_id(self):
        """Передает ID Кинопоиска"""
        a = self.plainTextEdit.toPlainText()
        text = "Некоректный ID, он должен состоять только из цифр"

        if 2 < len(a) < 20:
            try:
                int(a)
                self.user_id = a
                self.button_send_path_2.setStyleSheet("background-color: rgb(80, 255, 115);\n"
                                                      "color: rgb(0, 0, 0);\n")
            except:
                self.print_massage(text=text, side='error')
        else:
            self.print_massage(text=text, side='error')

    def func_send_path(self):
        """Передает путь для сохранения файлов"""
        self.path_file = QFileDialog.getExistingDirectory()
        if self.path_file.endswith('/'):
            self.path_file = self.path_file[0:-1]
        if len(self.path_file) > 0:
            self.button_send_path.setStyleSheet("background-color: rgb(80, 255, 115);\n"
                                                "color: rgb(0, 0, 0);\n")

    def func_start_download(self, user_id=None, path_file=None):
        """Парсинг Кинопоиска"""
        if user_id == None or path_file == None:
            text = "Не указан путь для сохранения или ID"
            self.print_massage(text=text, side='error')

        else:
            text = f'''Для парсинга Ваших оценок с Кинопоиска, возможно понадобиться пройти проверку на то что вы человек. Не закрывайте открытый браузер программой!'''
            self.print_massage(text)

            for i in range(3):
                flag = False
                try:
                    a = VirtualBrowser(user_id, path_file)
                    a.start_parsing()
                    flag = True
                    break
                except Exception as e:
                    print(e)
                    continue
            if flag == True:
                text = f'''Парсинг успешно завершен. Файлы сохранены в папку {path_file}'''
                self.print_massage(text)

            else:
                text = """Произошла ошибка при парсинге данных. Проверьте открываться ли у Вас сайт Кинопоиска, возможно нужен VPN. Проверьте правильность ID. Попробуйте позже, если опять будет ошибка напишите в тех. поддержку - rocky01396@gmail.com"""
                self.print_massage(text=text, side='error')

    def func_start_rate(self, user_id, path_file):
        """Проставляет оценки на IMDB"""
        try:
            with open(self.path_file + '/mov_dict.json', 'r', encoding='utf-8') as file:
                file = json.load(file)
                for n, i in enumerate(file):
                    continue

                def popup_clicked(i):

                    if 'No' in i.text():
                        self.func_start_download(user_id, path_file)

                massage = QMessageBox()
                massage.setWindowTitle('Важно!')
                massage.setText(
                    f'''Найден файл с оценками, в котором {n} оценок. Если вы уже начинали проставлять оценки, они продолжат проставляться с места последней остановки. Желаете использовать этот файл? Если ответите NO, оценки будут скачаны заново с Кинопоиск и проставляться тоже будут заново''')
                massage.setIcon(QMessageBox.Question)
                massage.setWindowIcon(QtGui.QIcon('icon.ico'))
                massage.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                massage.buttonClicked.connect(popup_clicked)
                massage.exec_()


        except:
            self.func_start_download(user_id, path_file)

        finally:
            text = f"""Для проставления оценок на Ваш IMDB, понадобиться пройти авторизацию на сайте. Сам процесс занимает время, так как каждый фильм проставляется отдельно. В среднем на один фильм уходит 3 сек, 1000 фильмов займет около 50 мин:-)"""
            self.print_massage(text)

            try:
                a = VirtualBrowser(user_id, path_file)
                a.start_rate_imdb()

                text = f"""Файл с ошибками (если они были) сохранен в папку {path_file}"""
                self.print_massage(text)

            except Exception as e:
                print(e)
                text = "Произошла ошибка при проставлении оценок. Попробуйте позже, если опять будет ошибка напишите в тех. поддержку - rocky01396@gmail.com"
                self.print_massage(text=text, side='error')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
