from typing import List, Any
from prompt import prompt
from core import MangaDex
from core.config import CONF


def clear_term():
    print('\033c', end='')


def search(client: ExHentai, query: str):
    path = '/manga'
    params = {'title': query, 'limit': 100}

    return client.request(path, params)['data']


def parse_chapters(client: ExHentai, id: str):
    path = '/manga/{}/feed'.format(id)
    params = {'limit': 500, 'translatedLanguage[]': ['en']}

    return client.request(path, params)['data']


def picker(array: List[Any], title: str, multiselect: bool = False):
    title = '{}\nType "help" to get help, blank Enter to complete'.format(
        title
    )
    selected = prompt(
        array, title, multiselect, CONF.paginate, CONF.lines_per_page
    )

    return selected


def yes_no(prompt: str = 'Your choice:'):
    response = input(prompt + ' [y/n]').strip().lower()
    if response in ['yes', 'ye', 'y']:
        return True
    else:
        return False
