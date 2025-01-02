from typing import List
from core.helpers import picker


def fetch_en(data):
    try:
        return data['en']
    except KeyError:
        return data


class Tag:
    def __init__(self, id: str, name: str, description: str, group: str):
        self.id = id
        self.name = name
        self.description = description
        self.group = group

    def __str__(self):
        return self.name


class TagList:
    def __init__(self):
        self.tags: List[Tag] = []

    def build_list(self, data: List[dict]):
        for raw_data in data:
            attr = raw_data['attributes']

            id = raw_data['id']
            name = fetch_en(attr['name'])
            description = fetch_en(attr['description'])
            group = attr['group']

            tag = Tag(id, name, description, group)
            self.tags.append(tag)

    def __str__(self):
        return ', '.join([str(tag) for tag in self.tags])


class Chapter:
    def __init__(
        self, id: str, title: str, volume: str, pages: str, chapter: str
    ):
        self.id = id
        self.host: str = ''
        self.title = str(title)
        self.volume = volume
        self.pages = pages
        self.chapter = chapter

    def download_chapter(self):
        pass


class ChapterList:
    def __init__(self):
        self.chapters: List[Chapter] = []

    def build_list(self, data: dict):
        for raw in data:
            attr = raw['attributes']

            chapter = Chapter(
                raw['id'],
                attr['title'],
                attr['volume'],
                attr['pages'],
                attr['chapter'],
            )

            self.chapters.append(chapter)

    def choose(self):
        # Sort the title by its chapter
        # Pretty simple, right?
        titles = [
            'Chapter ' + chapter.chapter + ': ' + chapter.title
            for chapter in sorted(
                self.chapters, key=lambda chapter: float(chapter.chapter)
            )
        ]
        _, index = picker(titles, 'Pick some to preview: ', True)

        return self.chapters[index]


class Manga:
    # Represent a manga
    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        status: str,
        tags: TagList,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.tags = tags
        # self.chapters: ChapterList = None,

    def preview(self):
        print(
            '---\n{}\nStatus: {}\n---\nDescription:\n{}\n---\nTags: {}'.format(
                self.title, self.status, self.description, str(self.tags)
            )
        )


class MangaList:
    # Represent the manga list that we got after searching
    def __init__(self):
        self.mangas: List[Manga] = []

    def build_list(self, data: dict):
        for raw in data:
            attr = raw['attributes']
            tag_list = TagList()
            tag_list.build_list(attr['tags'])

            manga = Manga(
                raw['id'],
                fetch_en(attr['title']),
                fetch_en(attr['description']),
                attr['status'],
                tag_list,
            )

            self.mangas.append(manga)

    def choose(self):
        titles = [manga.title for manga in self.mangas]
        _, index = picker(titles, 'Pick one to preview: ')

        return self.mangas[index]
