from unittest import TestCase, mock

from requests import status_codes
from src.genius import GeniusApi
from types import SimpleNamespace
import responses


class TestGenius(TestCase):
    def setUp(self) -> None:
        self.configuration = SimpleNamespace(url="https://api.genius.com/",
                                             client_id="",
                                             client_secret="",
                                             access_token="")
        self.genius_api = GeniusApi(self.configuration)

    @responses.activate
    def test_genius_artist(self):
        responses.add(responses.GET,
                      self.configuration.url,
                      json={
                          'meta': {
                              'status': 200
                          },
                          'response': ["1234"]
                      })

        resp = self.genius_api.get_artist("bad bunny")
        assert resp == ["1234"]
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == "https://api.genius.com/?q=bad%20bunny"

    @responses.activate
    def test_genius_artist_unauthorized(self):
        responses.add(responses.GET,
                      self.configuration.url,
                      json={
                          'meta': {
                              'status': 401
                          },
                          'response': []
                      },
                      status=401)

        resp = self.genius_api.get_artist("bad bunny")
        assert resp == {}
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == "https://api.genius.com/?q=bad%20bunny"

    def tearDown(self) -> None:
        pass
