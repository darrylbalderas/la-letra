from .config import Configuration
import requests
from http import HTTPStatus
from pprint import pprint


class GeniusApi:
    def __init__(self, configuration: Configuration) -> None:
        self.configuration = configuration

    def _verify_request(self, response):
        try:
            status_code = response["meta"]["status"]
            if status_code != HTTPStatus.ACCEPTED and status_code != HTTPStatus.OK:
                return HTTPStatus.UNAUTHORIZED, {}
        except Exception:
            return HTTPStatus.BAD_REQUEST, {}
        return HTTPStatus.OK, response["response"]

    def _perform_get_request(self, url, parameters=None):
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + self.configuration.access_token,
        }
        if parameters:
            url = f'{url}?q={"%20".join(parameters.split())}'

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

    def artist_id(self, query):
        url = f"{self.configuration.url}/search"
        _, response = self._perform_get_request(url, parameters=query)

        if not response:
            return []

        artists = [
            h["result"].get("primary_artist") for h in response["hits"]
            if h["result"].get("primary_artist")
        ]

        return self.possible_artist_id(artists)

    def artist_lyrics_url(self, artist_name: str):
        artist_id = self.artist_id(artist_name)
        url = f"{self.configuration.url}/artists/{artist_id}/songs"
        _, response = self._perform_get_request(url)

        if not response:
            return []

        # TODO: Make requests to grab all the pages

        # TODO: Filter response to get only primary artist that matches artist name

        return [s['url'] for s in response['songs']]