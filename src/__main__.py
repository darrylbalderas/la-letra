from pprint import pprint
from .config import Configuration

from .genius import GeniusApi


def main():
    genius_api = GeniusApi(configuration=Configuration())
    lyric_urls = genius_api.artist_lyrics_url("bad bunny")

    pprint(lyric_urls)

    # TODO: Create scaper to gather lyrics from genius


if __name__ == "__main__":
    main()
