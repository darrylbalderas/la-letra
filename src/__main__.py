from .config import Configuration

from .genius import GeniusApi


def main():
    genius_api = GeniusApi(configuration=Configuration())
    artist = genius_api.get_artist("bad bunny")
    print(artist)


if __name__ == "__main__":
    main()
