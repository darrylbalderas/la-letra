import requests
import os


class Configuration:
    def __init__(self) -> None:
        self.url = self.validate_env("GENIUS_URL")
        self.client_id = self.validate_env("CLIENT_ID")
        self.client_secret = self.validate_env("CLIENT_SECRET")
        self.access_token = self.validate_env("ACCESS_TOKEN")

    def validate_env(key):
        value = os.environ.get("key")
        if not value:
            raise RuntimeError(f"Missing {key} environment variable")
        return value

    @property
    def url(self):
        return self.url

    @property
    def client_id(self):
        return self.client_id

    @property
    def client_secret(self):
        return self.client_secret

    @property
    def access_token(self):
        return self.access_token


class GeniusParser:
    def __init__(self, configuration) -> None:
        self.configuration = configuration

    def verify_request(response):
        try:
            status_code = response["meta"]["status"]
            if status_code != 202 or status_code != 200:
                return 401, {}
        except Exception:
            return 400, {}
        return 200, response["response"]

    def _perform_request(self, parameters=None):
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + self.configuration.access_token,
        }
        if parameters:
            url = f'{self.configuration.url}?q={"%20".join(parameters.split())}'
        else:
            url = self.configuration.url

        return self.verify_request(requests.get(url, headers=headers).json())

    def possible_artist_id(primary_artists):
        if len(primary_artists) == 0:
            return None
        counts = {}
        max_id = primary_artists[0]["id"]
        counts[max_id] = 1
        for primary_artist in primary_artists:
            artist_id = primary_artist["id"]
            if artist_id not in counts:
                counts[artist_id] = 1
            counts[artist_id] += 1
            if counts[artist_id] > counts[max_id]:
                max_id = artist_id
        return max_id

    def get_artist_id(self, query):
        """Extract artist id from search results for a particular artist"""
        status_code, data = self._perform_response(parameters=query)
        artists = []
        for hit in data["hits"]:
            artist = hit["result"].get("primary_artist")
            if artist:
                artists.append(artist)
        artist_id = self.possible_artist_id(artists)
        return artist_id

    def lyrics():
        pass

    def artists():
        pass

    def songs():
        pass


def main():
    pass


if __name__ == "__main__":
    main()
