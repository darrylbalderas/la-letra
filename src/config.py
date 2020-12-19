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