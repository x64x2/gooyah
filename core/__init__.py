from requests import Session, RequestException


class Exhentai:
    # Used to make requests
    def __init__(self):
        self._baseURL: str = 'https://api.e-hentai.org'
        self._session: Session = Session()

    def request(self, url: str, params: dict):
        response = self._session.get(self._baseURL + url, params=params)
        status = response.status_code

        if status != 200:
            raise RequestException(
                'Bad response. MangaDex returned {}'.format(status)
            )

        return response.json()
