from bs4 import BeautifulSoup

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class LyricParser:
    def __init__(self, download_location=None) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280x1696')
        chrome_options.add_argument('--user-data-dir=/tmp/user-data')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--log-level=0')
        chrome_options.add_argument('--v=99')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--data-path=/tmp/data-path')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--homedir=/tmp')
        chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

        # chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"
        self._driver = webdriver.Chrome(ChromeDriverManager().install())
        # self._driver = webdriver.Chrome(
        #                                 chrome_options=chrome_options)

    def validate_tags(self, tag):
        "Remove tags that are not text or anchor tags"
        is_break = tag.name == 'br' or tag.name == 'defer-compile'
        is_lyric_section = tag.name is None and tag.startswith('[')
        return is_break or is_lyric_section

    def parse_tag(self, tag):
        # TODO: Create a Lyric object that holds link, text and category
        is_anchor = tag.name == 'a'
        return tag if not is_anchor else tag.text

    def apply(self, url):
        self._driver.get(url)
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        html_content = soup.select("p")[0]
        return [self.parse_tag(tag) for tag in html_content if self.validate_tags(tag)]

    def close(self):
        self._driver.quit()
