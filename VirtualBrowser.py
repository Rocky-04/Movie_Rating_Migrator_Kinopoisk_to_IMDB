import json
import pickle
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait


class VirtualBrowser:
    def __init__(self, user_id, path_file=''):
        self.user_id = user_id
        self.path_file = path_file

    def start_parsing(self):
        'Парсинг оценок пользователя в EXCEL, Json'
        self.name_movie_rus = []
        self.name_movie = []
        self.my_grade = []
        self.week = []
        self.count_grey = []
        self.id_kinopoisk = []
        self.rating_kinopoisk = []
        self.id_imdb = []
        self.d = {'name_movie_rus': self.name_movie_rus,
                  'name_movie': self.name_movie,
                  'my_grade': self.my_grade,
                  'week': self.week,
                  'count_grey': self.count_grey,
                  'id_kinopoisk': self.id_kinopoisk,
                  'rating_kinopoisk': self.rating_kinopoisk,
                  "id_imdb": self.id_imdb}

        self.start_browser_kinopoisk()
        self.top_movies = self.read_file('tom_movies_20000.json')

        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        a = int(soup.find('div', class_='pagesFromTo').text.split(' из ')[1])  # узнаем сколько оценок
        for i in range(1, (a // 200) + 2):  # Парсим оценки
            try:
                url = f'https://www.kinopoisk.ru/user/{self.user_id}/votes/list/ord/date/page/{i}/#list'
                print(f'Извлекаю страницу №{i} - {url}')
                time.sleep(5)
                self.browser.get(url)
                wait(self.browser, 600).until(
                    EC.url_contains(f'https://www.kinopoisk.ru/user/{self.user_id}/votes/list'))
            except:
                self.browser.refresh()
                url = f'https://www.kinopoisk.ru/user/{self.user_id}/votes/list/ord/date/perpage/200/page/{i}/#list'
                print(f'Извлекаю страницу №{i} - {url}')
                time.sleep(5)
                self.browser.get(url)
                wait(self.browser, 600).until(
                    EC.url_contains(f'https://www.kinopoisk.ru/user/{self.user_id}/votes/list'))
            self.parsing_page()
        self.browser.quit()

        file = self.path_file + '/movie_list.xlsx'  # сохраняю оценки в xlsx
        with open(file, 'w') as xlsx:
            data = pd.DataFrame(self.d)
        data.to_excel(file)
        print('Файл с оценками успешно сохранен в формате xlsx')

        mov_dict = {}
        for i in range(len(self.id_kinopoisk)):
            mov_dict[self.id_kinopoisk[i]] = {}
            mov_dict[self.id_kinopoisk[i]]['my_grade'] = self.my_grade[i]
            mov_dict[self.id_kinopoisk[i]]['id_imdb'] = self.id_imdb[i]
            mov_dict[self.id_kinopoisk[i]]['name_movie_rus'] = self.name_movie_rus[i]

        file = self.path_file + '/mov_dict.json'  # сохраняю оценки в json
        with open(file, 'w', encoding="utf-8") as f:
            json.dump(mov_dict, f, indent=3, ensure_ascii=False)
            print('Файл успешно сохранен в формате json')

    def start_browser_kinopoisk(self):
        """Запускаю браузер для парсинга с кинопоиска"""
        self.browser = Chrome('chrome/chromedriver.exe')
        self.browser.get(f'https://www.kinopoisk.ru/user/{self.user_id}/votes/list/ord/date/perpage/200/page/1/#list')

        # Загружем куки
        for cookie in pickle.load(open('chrome/session', 'rb')):
            self.browser.add_cookie(cookie)
        url = f'https://www.kinopoisk.ru/user/{self.user_id}/votes/list/ord/date/perpage/200/page/1/#list'
        self.browser.get(url)

    def read_file(self, file: str):
        """Считываю содержимое файла"""
        with open(file, 'r', encoding="utf-8") as json_file:
            movies = json.load(json_file)
            return movies

    @staticmethod
    def examination_count_grade(a: list):
        """Удаление лишних символов и преобразование  к верному формату"""
        num = ''
        a = ''.join(a)
        a = a[a.find('('):a.find(')') + 1]
        for i in a:
            if i in '0123456789':
                num += i
        return num

    def parsing_page(self):
        """Парсинг данных с Кинопоиска"""
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        films = soup.find('div', class_='profileFilmsList').findAll('div', class_='item')
        for film in films:
            # try:
            self.name_movie.append(film.find('div', class_='info').find('div', class_='nameEng').text)
            self.my_grade.append(film.find('div', class_='vote').text)
            self.count_grey.append(self.examination_count_grade(film.find('div', class_='rating').text.strip()))
            n = str(film.find('div', class_='info').find('div', class_='nameRus').text)
            self.name_movie_rus.append(n[:n.find('(')])
            self.week.append(n[-5:-1:1])
            a = str(film.find('div', class_='selects vote_widget'))
            id = a[a.find('rating_user_') + 12: a.find('"', (a.find('rating_user_') + 13))]
            self.id_kinopoisk.append(id)
            x = film.find('div', class_='rating').text[1:6]

            try:
                # Узнаем id_imdb.
                if id in self.top_movies:  # 1. Пробуем найти в файле
                    imdb = self.top_movies[id]['id_imdb']
                else:  # 2. Пробуем спарсить с API kinobd
                    api = self.start_api_kinobd(id)
                    imdb = api['data'][0]['imdb_id'] if api != None else None
                    if imdb == None:  # 3. Пробуем найти в API kinopoiskapiunofficial
                        api = self.start_api(id)
                        imdb = api['imdbId'] if api != None else None
                self.id_imdb.append(imdb)
            except Exception as e:
                self.id_imdb.append(None)
                print(e)

            try:
                x = float(x)
                self.rating_kinopoisk.append(x)
            except:
                self.rating_kinopoisk.append(None)

    def start_api(self, id):
        """Получаем данные с апи kinopoiskapiunofficial"""
        key_lst = ['3cdf0f0f-62f5-4840-b0d6-3f0a047f3dcb', '44535d0b-6460-4480-ab4c-c4ff53dbccf0',
                   'ba6a0687-09dd-4268-8d23-c91114f82203', 'bd698eba-576a-4145-9fa1-4be16d8f9d74',
                   '472717ab-55ca-4a8f-b486-c6d2ba55ddda', '777397b3-cc2b-4fc0-b2f2-4116b03d95f8',
                   'cddbfaa8-b837-443f-9b49-d162995a8c7d', '768ddd36-3b0f-47fb-a0a2-9640319aa036',
                   '32a98d34-bcdd-42d0-83d2-71c30b5dab4c', '586676af-5bf9-4dd8-8502-c835ac8631fe',
                   '08016bb5-85ae-4aab-a996-346c12e86aea', '57f12959-9b65-4e99-a6d2-7368dfb64730',
                   'd6728934-78a0-478c-a081-912b88bec29b', 'c2b1b8ce-e802-4ebb-9fd7-38a36af09bca',
                   '3b44f759-0a94-4ae9-bc04-d23a3a29c461', 'b7541a2e-edfc-4baa-a870-9ba17f9a52ae',
                   'cae6b836-a4d9-43a7-bb9b-0e1a7042d5e8', 'f3763ff7-d47e-4550-ac98-fa007e6dd51e',
                   'd67d88a1-6e2d-4497-8c60-2bfefd96f358', '4f358e01-8636-4b70-b63d-d76a42451269',
                   '6294d1a3-c7e6-4de8-9cef-2c60bcdd0af0', 'f25a63cf-cd08-4a3b-be19-69c858dd6042',
                   'a951732e-564e-44e0-be11-c82ee1e79a8a', '127cf83f-2fd9-4699-a70a-7e023ea26c6b',
                   'e2465028-4dee-4e58-915d-f468cda96210']
        count_key = 0
        while True:
            try:
                try:
                    api = requests.get('https://kinopoiskapiunofficial.tech/api/v2.2/films/' + id,
                                       headers={'X-API-KEY': key_lst[count_key],
                                                'Content-Type': 'application/json'})

                    api = json.loads(api.content.decode('utf-8'))
                    return api
                except:
                    count_key += 1
                    if count_key > len(key_lst):
                        return None
                    api = requests.get('https://kinopoiskapiunofficial.tech/api/v2.2/films/' + id,
                                       headers={'X-API-KEY': key_lst[count_key],
                                                'Content-Type': 'application/json'})

                    api = json.loads(api.content.decode('utf-8'))
                    return api
            except Exception as e:
                print(e)
                return None

    def start_api_kinobd(self, id):
        """Получаем данные с апи kinobd.net"""
        try:
            api = requests.get(f'https://kinobd.net/api/films/search/kp_id?q={id}', headers={'User-Agent': 'Rock'})
            api = json.loads(api.content.decode('utf-8'))
            return api
        except Exception as e:
            print(e)
            return None

    def start_rate_imdb(self):
        """Проставляем оценки на IMDB с json"""
        # Создаем файл для фильмов которым не удалось проставить оценки
        errors = []
        movies = self.read_file(self.path_file + '/mov_dict.json')
        # Запускаю браузер
        self.browser = Chrome('chrome/chromedriver.exe')
        # Переходим на страницу авторизации
        self.browser.get(f'https://www.imdb.com/registration/signin?ref=nv_generic_lgin&u=%2F')
        # Ждем авторизацию пользователя
        wait(self.browser, 600).until(EC.url_contains('https://www.imdb.com/?ref_=login'))
        # Получаю куки для авторизации
        pickle.dump(self.browser.get_cookies(), open('chrome//session_imdb', 'wb'))
        # Запускаю браузер с настройками и куками
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        self.browser = Chrome('chrome/chromedriver.exe', options=options)
        self.browser.get('https://www.imdb.com')
        for cookie in pickle.load(open('chrome\\session_imdb', 'rb')):
            self.browser.add_cookie(cookie)

        # Проставляем оценки
        for movie in movies:
            try:
                if movies[movie]['id_imdb'] == None:
                    errors.append(
                        [movie, movies[movie]['name_movie_rus'], f"должна быть оценка {movies[movie]['my_grade']}",
                         f'Не найдено соответствие фильма на IMDB'])
                else:
                    answer = self.rate_id_imdb(movies[movie]['id_imdb'], movies[movie]['my_grade'])
                    if answer == False:
                        errors.append(
                            [movie, movies[movie]['name_movie_rus'], f"должна быть оценка {movies[movie]['my_grade']}",
                             f'https://www.imdb.com//title//{movies[movie]["id_imdb"]}'])
            except Exception as e:
                print(e, movies[movie]['name_movie_rus'])
                errors.append(
                    [movie, movies[movie]['name_movie_rus'], f"должна быть оценка {movies[movie]['my_grade']}",
                     f'https://www.imdb.com//title//{movies[movie]["id_imdb"]}'])

        # создаем файл с ошибками
        if len(errors) > 0:
            file = self.path_file + 'errors.xlsx'  # сохраняю оценки в xlsx
            with open(file, 'w') as xlsx:
                data = pd.DataFrame(errors)
            data.to_excel(file)
            print('Файл c ошибками успешно сохранен в формате xlsx')

        self.browser.quit()

    def rate_id_imdb(self, film, grade):
        """Поставить оценку фильму на imdb
        Возвращает True если оценка успешно проставлена"""

        answer = True
        browser = self.browser
        try:
            browser.switch_to.new_window()
            url = 'https://www.imdb.com/title/' + film
            browser.get(url)
        except Exception as e:
            print(e)
            print(f'{film} - не удалось получить Веб страницу')
        time.sleep(1)
        try: #Проверка: стоит ли уже верная оценка
            if browser.find_element(By.XPATH,
                                    '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[2]/button/div/div/div[2]/div/span').text == grade:
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
                return answer
        except:
            answer = False
        try: #Ставим оценку

            browser.find_element(By.XPATH,
                                 '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[2]/button').click()
            time.sleep(1)
            element = browser.find_element(By.XPATH,
                                           f'/html/body/div[4]/div[2]/div/div[2]/div/div[2]/div[2]/div/div[2]/button[{grade}]')
            ActionChains(browser).move_to_element(element).click().perform()
            browser.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[2]/div/div[2]/div[2]/button').click()
            time.sleep(1)
            answer = True if browser.find_element(By.XPATH,
                                                  '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[2]/button/div/div/div[2]/div/span').text == grade else False
        except:
            print(f'{"https:/www.imdb.com/title/" + film} - возможно произошла ошибка. Должна быть оценка {grade}')
            answer = False
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        return answer
