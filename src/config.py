import os


class Configuration:
    def __init__(self) -> None:
        self._url = self.validate_env("GENIUS_URL")
        self._client_id = self.validate_env("CLIENT_ID")
        self._client_secret = self.validate_env("CLIENT_SECRET")
        self._access_token = self.validate_env("ACCESS_TOKEN")

    def validate_env(self, key):
        value = os.environ.get(key)
        if not value:
            raise RuntimeError(f"Missing {key} environment variable")
        return value

    @property
    def url(self):
        return self._url

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret

    @property
    def access_token(self):
        return self._access_token