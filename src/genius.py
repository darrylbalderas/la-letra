from .config import Configuration
import requests
from http import HTTPStatus


class GeniusApi:
    def __init__(self, configuration: Configuration) -> None:
        self.configuration = configuration

    def _verify_request(self, response):
        try:
            status_code = response["meta"]["status"]
            if status_code != HTTPStatus.ACCEPTED and status_code != HTTPStatus.OK:
                return HTTPStatus(status_code), {}
        except Exception:
            return HTTPStatus(response["meta"]["status"]), {}
        return HTTPStatus.OK, response["response"]

    def _perform_get_request(self, url, parameters=None):
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + self.configuration.access_token,
        }
        if parameters:

            url_parameters = []
            for k, v in parameters.items():
                url_parameters.append(f"{k}={v}")
            url = f'{url}?{"&".join(url_parameters)}'

        return self._verify_request(requests.get(url, headers=headers).json())

    def possible_artist_id(self, artists):
        if len(artists) == 0:
            return None
        frequency = {}
        possible_id = artists[0]["id"]
        frequency[possible_id] = 1
        for primary_artist in artists:
            artist_id = primary_artist["id"]

            if artist_id not in frequency:
                frequency[artist_id] = 0

            frequency[artist_id] += 1

            if frequency[artist_id] > frequency[possible_id]:
                possible_id = artist_id
        return possible_id

    def artist_id(self, artist_name):
        url = f"{self.configuration.url}/search"
        parameters = {'q': "%20".join(artist_name.split())}
        _, response = self._perform_get_request(url, parameters=parameters)

        if not response:
            return []

        artists = [
            h["result"].get("primary_artist") for h in response["hits"]
            if h["result"].get("primary_artist")
        ]

        return self.possible_artist_id(artists)

    def is_primary_artist(self, song, artist_id):
        return song['primary_artist']['id'] == artist_id

    def is_original(self, song):
        pyongs_count = song['pyongs_count']
        annotation_count = song['annotation_count']
        is_pyongs_count = pyongs_count is not None and pyongs_count > 0
        is_annotation_count = annotation_count is not None and annotation_count > 0
        return '(' not in song['title'] and is_pyongs_count and is_annotation_count

    def artist_lyrics_url(self, artist_name: str):
        artist_id = self.artist_id(artist_name)
        if not artist_id:
            return []
        url = f"{self.configuration.url}/artists/{artist_id}/songs"
        current_page = 1
        # TODO: Move this to configuration
        num_pages = 8
        status_code = HTTPStatus.OK
        lyrics_urls = []
        while status_code == HTTPStatus.OK and current_page <= num_pages:
            status_code, response = self._perform_get_request(url,
                                                              parameters={
                                                                  'sort': 'popularity',
                                                                  'page': current_page
                                                              })
            if not response:
                return lyrics_urls

            for song in response['songs']:
                if self.is_primary_artist(song, artist_id) and self.is_original(song):
                    lyrics_urls.append(song['url'])

            current_page += 1
        return lyrics_urls
