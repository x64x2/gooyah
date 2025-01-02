from core import MangaDex
from core.lists import MangaList, ChapterList
from core.helpers import search, parse_chapters, clear_term, yes_no
from core.config import CONF


def run_loop():
    client = MangaDex()

    while True:
        clear_term()
        query = input('Search for a manga: ')

        if len(query.strip()) < 1:
            print("No actions made. Aborting...")
            break

        response = search(client, query)
        manga_list = MangaList()
        manga_list.build_list(response)

        # There might be an independent loop here
        while True:
            try:
                manga = manga_list.choose()
            except ValueError:
                break

            clear_term()
            manga.preview()

            if not yes_no('List chapters?'):
                continue

            response = parse_chapters(client, manga.id)
            chapter_list = ChapterList()
            chapter_list.build_list(response)

            while True:
                try:
                    chapter = chapter_list.choose()
                except ValueError:
                    break


if __name__ == '__main__':
    CONF.parse()
    print('Starting CLI...')
    run_loop()
