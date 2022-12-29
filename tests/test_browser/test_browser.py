import pytest


@pytest.mark.parametrize('grades, result', [
    ("7.016 (6 134) 21", "6134"),
    ("6.126 (106 363) 123 мин.", "106363"),
    ("7.639 (52 490) 96 мин.", "52490"),
])
def test_clean_grades(virtual_browser, grades, result):
    assert virtual_browser.clean_grades(grades) == result


@pytest.mark.parametrize('kinopoisk_id, result', [
    ("1044592", "tt1072748"),
    ("409178", "tt1139592"),
    ("730709", "tt2620590"),
])
def test_fetch_film_data_from_api_unofficial(virtual_browser, kinopoisk_id, result):
    answer = virtual_browser.fetch_film_data_from_api_unofficial(kinopoisk_id)['imdbId']
    assert answer == result


@pytest.mark.parametrize('kinopoisk_id, result', [
    ("1044592", "tt1072748"),
    ("409178", "tt1139592"),
    ("730709", "tt2620590"),
])
def test_fetch_film_data_from_api_kinobd(virtual_browser, kinopoisk_id, result):
    answer = virtual_browser.fetch_film_data_from_api_kinobd(kinopoisk_id)['data'][0]['imdb_id']
    assert answer == result
