from pprint import pprint
from .config import Configuration

from .genius import GeniusApi
from src.scaper import LyricParser


def main():
    genius_api = GeniusApi(configuration=Configuration())
    lyric_urls = genius_api.artist_lyrics_url("bad bunny")

    # TODO: Add context manager patter to lyric parser
    lyric_parser = LyricParser()

    song_lyrics = []
    for url in lyric_urls:
        song_lyrics.append(lyric_parser.apply(url))

    lyric_parser.close()

    # TODO: Store lyrics in S3


if __name__ == "__main__":
    main()
