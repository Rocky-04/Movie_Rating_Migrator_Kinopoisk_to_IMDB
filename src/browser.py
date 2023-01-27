import json
import os
import pickle
import time
from typing import Union

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as Wait

from data.API import API_KINOBD
from data.API import API_UNOFFICIAL_ENDPOINT
from data.API import API_UNOFFICIAL_KEY_HEADER
from data.API import KEYS_KINOPOISK_API_UNOFFICIAL
from data.API import USER_AGENT_HEADER


class VirtualBrowser:
    DRIVER_PATH = '../chrome_driver/chromedriver.exe'
    TOP_MOVIES_PATH = '../data/top_movies_25000.json'
    URL_KINOPOISK = 'https://www.kinopoisk.ru/user/'

    def __init__(self, user_id: int, path_file: str = '') -> None:
        """
        Initialize a new VirtualBrowser object.

        :param user_id: the ID of the user whose ratings will be parsed
        :param path_file: (optional) the file path where the ratings will be saved
        """
        self.user_id = user_id
        self.path_file = path_file

        # Initialize variables
        self.russian_movie_names = []
        self.english_movie_names = []
        self.user_ratings = []
        self.weeks = []
        self.user_rating_count = []
        self.kinopoisk_ids = []
        self.kinopoisk_ratings = []
        self.imdb_ids = []
        self.rating_data = {'russian_movie_names': self.russian_movie_names,
                            'english_movie_names': self.english_movie_names,
                            'user_ratings': self.user_ratings,
                            'weeks': self.weeks,
                            'user_rating_count': self.user_rating_count,
                            'kinopoisk_ids': self.kinopoisk_ids,
                            'kinopoisk_ratings': self.kinopoisk_ratings,
                            "imdb_ids": self.imdb_ids}

        self.top_movies = {}

        # Initialize the Chrome browser
        self.browser = Chrome(self.DRIVER_PATH)

        # Initialize list of errors
        self.errors = []

    def parse_user_ratings(self) -> None:
        """
        Start parsing the user's ratings in EXCEL and JSON formats.

        :param self: the instance of the current object
        """
        # Launch the Kinopoisk browser and get the top movies list
        self.launch_kinopoisk_browser()
        self.top_movies = self.load_json_file(self.TOP_MOVIES_PATH)

        # Parse the user's ratings from the Kinopoisk website
        self.parse_ratings()

        # Save the ratings to an Excel file.
        self.export_ratings_to_excel()

        # Save the ratings to a JSON file.
        self.export_ratings_to_json()

    def parse_ratings(self) -> None:
        """
        Parse the user's ratings from the Kinopoisk website.

        :param self: the instance of the current object
        """

        # Get the number of ratings
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        num_ratings = int(soup.find('div', class_='pagesFromTo').text.split(' из ')[1])

        # Parse ratings
        for i in range(1, (num_ratings // 200) + 2):
            try:
                url = f'{self.URL_KINOPOISK}{self.user_id}/votes/list/ord/date/page/{i}/#list'
                print(f'Retrieving page {i} - {url}')
                time.sleep(2)
                self.browser.get(url)
                Wait(self.browser, 600).until(
                    ec.url_contains(f'{self.URL_KINOPOISK}{self.user_id}/votes/list'))
            except Exception as error:
                print(error)
                self.browser.refresh()
                url = (f'{self.URL_KINOPOISK}{self.user_id}/'
                       f'votes/list/ord/date/perpage/200/page/{i}/#list')
                print(f'Retrieving page {i} - {url}')
                time.sleep(2)
                self.browser.get(url)
                Wait(self.browser, 600).until(
                    ec.url_contains(f'{self.URL_KINOPOISK}{self.user_id}/votes/list'))
            self.parse_data_from_kinopoisk()
        self.browser.quit()

    def export_ratings_to_excel(self) -> None:
        """
        Save the ratings to an Excel file.

        :param self: the instance of the current object
        """

        file = self.path_file + '/movie_list.xlsx'  # save ratings in xlsx
        with open(file, 'w'):
            data = pd.DataFrame(self.rating_data)
        data.to_excel(file)
        print('Ratings successfully saved to Excel file.')

    def export_ratings_to_json(self) -> None:
        """
        Save the ratings to a JSON file.

        :param self: the instance of the current object
        """

        # Create dictionary of ratings
        rating_data = {}
        for i in range(len(self.kinopoisk_ids)):
            rating_data[self.kinopoisk_ids[i]] = {}
            rating_data[self.kinopoisk_ids[i]]['user_ratings'] = self.user_ratings[i]
            rating_data[self.kinopoisk_ids[i]]['imdb_ids'] = self.imdb_ids[i]
            if self.english_movie_names[i]:
                rating_data[self.kinopoisk_ids[i]]['movie_name'] = self.english_movie_names[i]
            else:
                rating_data[self.kinopoisk_ids[i]]['movie_name'] = self.russian_movie_names[i]

        # Save dictionary to JSON file
        file = self.path_file + '/rating_data.json'
        with open(file, 'w') as fp:
            json.dump(rating_data, fp)
        print('Ratings successfully saved to JSON file.')

    def launch_kinopoisk_browser(self) -> None:
        """
        Launches a browser for parsing from Kinopoisk.

        :param self: the instance of the current object
        """

        # Set the url for the browser to visit
        url = (f'{self.URL_KINOPOISK}{self.user_id}'
               f'/votes/list/ord/date/perpage/200/page/1/#list')

        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument(
            "--disable-blink-features=AutomationControlled")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--log-level=3')
        options.add_argument('start-maximized')
        options.add_argument('--disable-infobars')
        options.add_argument("--disable-extensions")

        # Initialize the Chrome browser with the specified options
        self.browser = Chrome(self.DRIVER_PATH, options=options)

        # Navigate to the specified url
        self.browser.get(url)

        # Load the cookies
        with open('../data/session_kinopoisk', 'rb') as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                self.browser.add_cookie(cookie)

        # Navigate to the url again after loading the cookies
        self.browser.get(url)

    def launch_imdb_browser(self) -> None:
        """
        Launches a browser for IMDB.

        :param self: the instance of the current object
        """
        if not os.path.exists('session_imdb'):
            # Navigate to the login page
            self.browser.get(f'https://www.imdb.com/registration/signin?ref=nv_generic_lgin&u=%2F')

            # Wait for the user to login
            Wait(self.browser, 600).until(ec.url_contains('https://www.imdb.com/?ref_=login'))

            # Get the cookies for login
            pickle.dump(self.browser.get_cookies(), open('session_imdb', 'wb'))

        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-webgl")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-xss-auditor")
        options.add_argument("--disable-web-security")
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--log-level=3')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-infobars')
        options.add_argument("--disable-extensions")
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.headless = False  # Show the window or not
        options.add_argument("--window-size=1400,1000")
        self.browser = Chrome(self.DRIVER_PATH, options=options)
        self.browser.get('https://www.imdb.com')

        # Load the cookies
        for cookie in pickle.load(open('session_imdb', 'rb')):
            self.browser.add_cookie(cookie)

    def parse_data_from_kinopoisk(self) -> None:
        """
        Parse data from Kinopoisk.

        :param self: the instance of the current object
        """

        # Find all the films on the page
        films = self.get_films_from_page()

        # Iterate over the films
        for film in films:
            # Get the English movie name
            self.english_movie_names.append(self.get_english_movie_name(film))

            # Get the user rating
            self.user_ratings.append(self.get_user_rating(film))

            # Get the count of user ratings
            self.user_rating_count.append(self.get_user_rating_count(film))

            # Get the Russian movie name and the week
            russian_movie_name, week = self.get_russian_movie_name_and_week(film)
            self.russian_movie_names.append(russian_movie_name)
            self.weeks.append(week)

            # Get the Kinopoisk ID
            kinopoisk_id = self.get_kinopoisk_id(film)
            self.kinopoisk_ids.append(kinopoisk_id)

            # Get the Kinopoisk rating
            rating = self.get_kinopoisk_rating(film)

            # Get the IMDb ID
            imdb_id = self.get_imdb_id(kinopoisk_id)
            self.imdb_ids.append(imdb_id)

            # Convert the Kinopoisk rating to a float
            kinopoisk_rating = self.convert_rating_to_float(rating)
            self.kinopoisk_ratings.append(kinopoisk_rating)

    def get_imdb_id(self, kinopoisk_id: str) -> Union[str, None]:
        """
        Retrieve the IMDb ID for a movie with a given Kinopoisk ID.

        :param self: the instance of the current object
        :param kinopoisk_id: The Kinopoisk ID of the movie
        :return: The IMDb ID of the movie, or None if it could not be found
        """
        top_movies = self.top_movies
        # 1. Try to find the IMDb ID in the top movies dictionary
        if kinopoisk_id in top_movies:
            return top_movies[kinopoisk_id]['id_imdb']

        # 2. Try to retrieve the IMDb ID using the kinobd API
        try:
            api_response = self.fetch_film_data_from_api_kinobd(kinopoisk_id)
            if api_response is not None:
                return api_response['data'][0]['imdb_id']
        except (KeyError, IndexError, TypeError):
            pass

        # 3. Try to retrieve the IMDb ID using the kinopoiskapiunofficial API
        try:
            api_response = self.fetch_film_data_from_api_unofficial(kinopoisk_id)
            if api_response is not None:
                return api_response['imdbId']
        except (KeyError, IndexError, TypeError):
            pass

        # If the IMDb ID could not be found, return None
        return None

    def get_movie_name(self, kinopoisk_id: str) -> Union[str, None]:
        """
        Retrieve the russian name for a movie with a given Kinopoisk ID.

        :param self: the instance of the current object
        :param kinopoisk_id: The Kinopoisk ID of the movie
        :return: The russian name of the movie, or None if it could not be found
        """
        top_movies = self.top_movies

        # 1. Try to find the russian name in the top movies dictionary
        if kinopoisk_id in top_movies:
            return top_movies[kinopoisk_id]['name_movie_rus']

        # 2. Try to retrieve the russian name using the kinobd API
        try:
            api_response = self.fetch_film_data_from_api_kinobd(kinopoisk_id)
            if api_response is not None:
                return api_response['data'][0]['name_russian']
        except (KeyError, IndexError, TypeError):
            pass

        # 3. Try to retrieve the russian name using the kinopoiskapiunofficial API
        try:
            api_response = self.fetch_film_data_from_api_unofficial(kinopoisk_id)
            if api_response is not None:
                return api_response['nameRu']
        except (KeyError, IndexError, TypeError):
            pass

        # If the russian name could not be found, return None
        return None

    def get_films_from_page(self) -> list:
        """
        Parse the page source and return a list of films.

        :param self: the instance of the current object
        """
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        films = soup.find('div', class_='profileFilmsList').findAll('div', class_='item')
        return films

    def get_user_rating_count(self, film) -> str:
        """
        Get the count of user ratings from a film.

        :param self: the instance of the current object
        :param film: the film element
        """
        user_rating_count = self.clean_grades(film.find('div', class_='rating').text.strip())
        return user_rating_count

    def start_rate_imdb(self) -> None:
        """
        Automatically rate movies on IMDB, using data stored in a JSON file.

        If the 'imdb_ids' field is not present or is None, the movie will be skipped and added to a
         list of errors.
        If the rating could not be applied, the movie will also be added to the list of errors.
        A file containing the list of errors will be created at the end of the function.
        """
        self.launch_imdb_browser()

        # Load the JSON file
        movies = self.load_json_file(self.path_file + '/rating_data.json')

        print('Start grading...')

        # Iterate through the movies in the JSON file
        for movie in movies:
            # Skip movies that have already been rated successfully
            if 'success' in movies[movie]:
                continue

            # Get the IMDB ID of the movie
            imdb_id = movies[movie]['imdb_ids']
            user_ratings = movies[movie]['user_ratings']
            movie_name = movies[movie]['movie_name']
            if imdb_id is None:
                self.add_error(movie, movies[movie], 'IMDB ID not found for movie')
                continue

            try:
                # Attempt to rate the movie
                rating_success = self.rate_imdb_ids(imdb_id, user_ratings)
                if rating_success:
                    # If the rating was successful, mark the movie as success and update JSON file
                    movies[movie]['success'] = True
                    print(f"{movie_name} - rating of {user_ratings} successfully applied")

                    with open(self.path_file + '/rating_data.json', 'w', encoding='utf-8') as file:
                        json.dump(movies, file, indent=3, ensure_ascii=False)
                else:
                    # If the rating was not successful, add the movie to the list of errors
                    self.add_error(movie, movies[movie])

            except Exception as error:
                self.add_error(movie, movies[movie], str(error))

        # Create an errors file
        self.create_errors_file()

        self.browser.quit()

    def rate_imdb_ids(self, imdb_id, user_ratings) -> bool:
        """
        Rate a movie on IMDB.

        This function is used to apply a rating to a movie on IMDB, given the movie's IMDB
        ID and the desired rating.

        :param imdb_id: the IMDB ID of the movie
        :param user_ratings: the rating to be applied to the movie (1-10)
        :return: True if the rating was successfully applied, False otherwise
        """

        # Open the movie's IMDB page
        if not self.open_imdb_page(imdb_id):
            return False
        time.sleep(1)

        # Check if the correct rating is already applied
        if self.check_rating(user_ratings):
            return True

        # Apply the rating
        if not self.apply_rating(user_ratings):
            return False

        # Verify that the rating was applied successfully
        if not self.verify_rating(user_ratings):
            return False

        # Close the IMDB page and switch back to the original window
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])
        return True

    def create_errors_file(self) -> None:
        """
        Create an errors file with the given errors.

        :param self: the instance of the current object
        """
        errors = self.errors
        if len(errors) > 0:
            file = self.path_file + '/errors.xlsx'
            with open(file, 'w'):
                data = pd.DataFrame(errors)
            data.to_excel(file)
            print('Error file successfully saved in XLSX format.')

    def add_error(self, kinopoisk_id: str, data: dict, error_details: str = '') -> None:
        """
        Add an error to the list of errors. This function is used to record an error that
        occurred while attempting to rate a movie on IMDB.

        :param self: the instance of the current object
        :param kinopoisk_id: the kinopoisk ID of the movie
        :param data: a dictionary containing the imdb_ids, user_ratings, movie_name of the movie.
        :param error_details: (optional) additional details about the error
        """
        imdb_id = data['imdb_ids']
        user_ratings = data['user_ratings']
        movie_name = data['movie_name']

        if not movie_name:
            movie_name = self.get_movie_name(kinopoisk_id)

        if imdb_id:
            link_imdb = f'https://www.imdb.com/title/{imdb_id}'
        else:
            link_imdb = ''

        self.errors.append(
            [kinopoisk_id, imdb_id, movie_name,
             f"should have a rating of {user_ratings}", error_details, link_imdb])

        print(f'{kinopoisk_id}, {imdb_id}, {movie_name}, '
              f'should have a rating of {user_ratings}:: {link_imdb}, {error_details}')

    def open_imdb_page(self, imdb_id: str) -> bool:
        """
        Open the movie's IMDB page in a new window.

        :param imdb_id: the IMDB ID of the movie
        :return: True if the page was successfully opened, False otherwise
        """
        try:
            # Open the movie's IMDB page in a new window
            self.browser.switch_to.new_window()
            url = 'https://www.imdb.com/title/' + imdb_id
            self.browser.get(url)
            return True
        except Exception as error:
            print(f'{error}: {imdb_id} - Unable to retrieve web page')
            return False

    def check_rating(self, user_ratings: str) -> bool:
        """
        Check if the correct rating is already applied to the movie.

        :param user_ratings: the rating that is expected to be applied to the movie
        :return: True if the correct rating is already applied, False otherwise
        """
        try:
            # Check if the current rating matches the expected rating
            if self.browser.find_element(By.XPATH, (
                    '/html/body/div[2]/main/div/section[1]/section/div[3]/section/'
                    'section/div[2]/div[2]/div/div[2]/button/div/div/div[2]/div/'
                    'span')).text == user_ratings:
                # Close the IMDB page and switch back to the original window
                self.browser.close()
                self.browser.switch_to.window(self.browser.window_handles[0])
                return True
            else:
                return False
        except Exception as error:
            print(f'{error}: Unable to check rating')
            return False

    def apply_rating(self, user_ratings: str) -> bool:
        """
        Apply a rating to a movie on IMDB.

        :param user_ratings: the rating to be applied to the movie (1-10)
        :return: True if the rating was successfully applied, False otherwise
        """
        try:
            # Click the rating button
            self.browser.find_element(By.XPATH, (
                '/html/body/div[2]/main/div/section[1]/section/div[3]/section/'
                'section/div[2]/div[2]/div/div[2]/button')).click()
            time.sleep(1)
            # Select the desired rating
            element = self.browser.find_element(By.XPATH,
                                                (f'/html/body/div[4]/div[2]/div/div[2]/div/div[2]/'
                                                 f'div[2]/div/div[2]/button[{user_ratings}]'))
            ActionChains(self.browser).move_to_element(element).click().perform()
            # Click the rating button to save the rating
            self.browser.find_element(By.XPATH, ('/html/body/div[4]/div[2]/div/div[2]/div/div[2]/'
                                                 'div[2]/button')).click()
            return True
        except Exception as error:
            print(error)
            return False

    def verify_rating(self, user_ratings: str) -> bool:
        """
        Verify that the rating was successfully applied to the movie.

        :param user_ratings: the rating that was expected to be applied to the movie

        :return: True if the rating was successfully applied, False otherwise
        """
        try:
            # Check if the current rating matches the expected rating
            if self.browser.find_element(By.XPATH, (
                    '/html/body/div[2]/main/div/section[1]/section/'
                    'div[3]/section/section/div[2]/div[2]/div/div[2]'
                    '/button/div/div/div[2]/div/'
                    'span')).text == user_ratings:
                return True
            else:
                return False
        except NoSuchElementException:
            print('Unable to verify rating')
            return False

    @staticmethod
    def get_english_movie_name(film) -> str:
        """
        Get the English movie name from a film.

        :param film: the film element
        """
        english_movie_name = film.find('div', class_='info').find('div', class_='nameEng').text
        return english_movie_name

    @staticmethod
    def get_user_rating(film) -> str:
        """
        Get the user rating from a film.

        :param film: the film element
        """
        user_rating = film.find('div', class_='vote').text
        return user_rating

    @staticmethod
    def get_russian_movie_name_and_week(film) -> tuple:
        """
        Get the Russian movie name and the week from a film.

        :param film: the film element
        """
        russian_movie_name_and_week = str(film.find('div', class_='info').find(
            'div', class_='nameRus').text)
        russian_movie_name = russian_movie_name_and_week[:russian_movie_name_and_week.find('(')]
        week = russian_movie_name_and_week[-5:-1:1]
        return russian_movie_name, week

    @staticmethod
    def get_kinopoisk_id(film) -> str:
        """
        Get the Kinopoisk ID

        :param film: the film element
        """
        rating_html = str(film.find('div', class_='selects vote_widget'))
        kinopoisk_id = rating_html[
                       rating_html.find('rating_user_') + 12: rating_html.find(
                           '"', (rating_html.find('rating_user_') + 13))
                       ]
        return kinopoisk_id

    @staticmethod
    def get_kinopoisk_rating(film) -> str:
        """
        Get the Kinopoisk rating

        :param film: the film element
        """
        rating = film.find('div', class_='rating').text[1:6]
        return rating

    @staticmethod
    def fetch_film_data_from_api_unofficial(kinopoisk_id: str) -> Union[dict, None]:
        """
        Get film data from the kinopoiskapiunofficial API.

        :param kinopoisk_id: The ID of the film to fetch from the API.
        :return: A dictionary containing the film data if the request is successful,
            or None if the request fails or if the list of API keys is empty.
        """
        if not KEYS_KINOPOISK_API_UNOFFICIAL:
            return None

        for key in KEYS_KINOPOISK_API_UNOFFICIAL:
            try:
                # Make the API request using the current API key
                api = requests.get(API_UNOFFICIAL_ENDPOINT + kinopoisk_id,
                                   headers={API_UNOFFICIAL_KEY_HEADER: key,
                                            'Content-Type': 'application/json'})
                api = json.loads(api.content.decode('utf-8'))
                return api
            except (ConnectionError, json.JSONDecodeError) as error:
                print(error)
        return None

    @staticmethod
    def fetch_film_data_from_api_kinobd(kinopoisk_id: str) -> Union[dict, None]:
        """
        Get film data from the kinobd.net API.

        :param kinopoisk_id: The ID of the film to fetch from the API.
        :return: A dictionary containing the film data if the request is successful,
            or None if the request fails or if the ID is invalid or empty.
        """
        if not kinopoisk_id:
            return None
        try:
            # Make the API request
            api = requests.get(API_KINOBD + kinopoisk_id, headers=USER_AGENT_HEADER)
            api = json.loads(api.content.decode('utf-8'))
            return api
        except (ConnectionError, json.JSONDecodeError) as error:
            print(error)
            return None

    @staticmethod
    def load_json_file(file: str) -> dict:
        """
        Load the contents of a JSON file.

        :param file: the path to the JSON file
        :return: a dictionary containing the data from the JSON file
        """
        with open(file, 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
            data = dict(reversed(list(data.items())))
            return data

    @staticmethod
    def convert_rating_to_float(rating: str) -> Union[float, None]:
        """
        Convert a rating string to a float.

        :param rating: The rating string to be converted
        :return: The rating as a float, or None if it could not be converted
        """
        try:
            return float(rating)
        except ValueError:
            return None

    @staticmethod
    def clean_grades(grades: list) -> str:
        """
        Remove extra characters and convert to the correct format.

        :param grades: a list of grades
        :return: a string containing the processed grades
        """
        processed_grades = ''
        grades = ''.join(grades)
        # Extract the part of the string between the '(' and ')'
        grades = grades[grades.find('('):grades.rfind(')') + 1]
        for character in grades:
            if character.isdigit():
                processed_grades += character
        return processed_grades
