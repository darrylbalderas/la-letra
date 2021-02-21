from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time


class LyricParser:
    def __init__(self, download_location=None) -> None:
        # TODO: Add user-agent
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--enable-javascript')
        # chrome_options.add_argument(
        #     'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        #         (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
        # current directory
        chrome_driver = os.getcwd() + "/chromedriver"
        self.browser = webdriver.Chrome(chrome_options=chrome_options,
                                        executable_path=chrome_driver)

    def get_page_source(self, url):
        self.browser.refresh()
        self.browser.get(url)
        time.sleep(0.5)
        self.browser.refresh()
        return self.browser.page_source

    def get_lyrics(self, html_content, lyrics):
        for tag in html_content:
            if isinstance(tag, str) and not tag.startswith('['):
                lyrics.append(tag)
            elif tag.name == 'br' or tag.name == 'defer-compile':
                continue
            elif tag.name == 'a':
                self.get_lyrics(tag, lyrics)

    def apply(self, url):
        soup = BeautifulSoup(self.get_page_source(url), 'html.parser')
        html_content = soup.select("p")[0]
        lyrics = []
        self.get_lyrics(html_content, lyrics)
        return lyrics

    def close(self):
        self.browser.quit()
