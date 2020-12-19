from src.config import Configuration
import requests
from http import HTTPStatus


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

    def _perform_get_request(self, parameters=None):
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + self.configuration.access_token,
        }
        if parameters:
            url = f'{self.configuration.url}?q={"%20".join(parameters.split())}'
        else:
            url = self.configuration.url

        return self._verify_request(requests.get(url, headers=headers).json())

    # def possible_artist_id(primary_artists):
    #     if len(primary_artists) == 0:
    #         return None
    #     counts = {}
    #     max_id = primary_artists[0]["id"]
    #     counts[max_id] = 1
    #     for primary_artist in primary_artists:
    #         artist_id = primary_artist["id"]
    #         if artist_id not in counts:
    #             counts[artist_id] = 1
    #         counts[artist_id] += 1
    #         if counts[artist_id] > counts[max_id]:
    #             max_id = artist_id
    #     return max_id

    def get_artist(self, query):
        status_code, data = self._perform_get_request(parameters=query)
        if status_code != HTTPStatus.OK:
            return {}
        return data

        # artists = []
        # for hit in data["hits"]:
        #     artist = hit["result"].get("primary_artist")
        #     if artist:
        #         artists.append(artist)
        # artist_id = self.possible_artist_id(artists)
        # return artist_id
