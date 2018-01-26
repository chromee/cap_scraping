import re
import requests
import urllib.request
from bs4 import BeautifulSoup
from scripts.image import Image


class WebRequest:
    anime_title = ""
    story_no = ""

    @staticmethod
    def get_img_url(html_url, timeout=10):
        response = requests.get(html_url, allow_redirects=True, timeout=timeout)
        soup = BeautifulSoup(response.text)
        img_url_array = [link.get('src') for link in soup.find_all('img')]

        title = soup.find("h1", class_="article-title").string
        global anime_title, story_no
        anime_title = re.search(r"【(?P<name>.*)】", title).group("name")
        story_no = re.search(r"第(?P<no>.*)話", title).group("no")
        return img_url_array

    @staticmethod
    def get_img_size(url):
        response = urllib.request.urlopen(url)
        size = (-1, -1)
        if response.status == 200:
            signature = response.read(2)
            if signature == b'\xff\xd8':  # jpg
                size = Image.parse_jpeg(response)
            elif signature == b'\x89\x50':  # png
                size = Image.parse_png(response)
            elif signature == b'\x47\x49':  # gif
                size = Image.parse_gif(response)
        response.close()
        return size

    @staticmethod
    def download(img_url, timeout=10):
        response = requests.get(img_url, allow_redirects=True, timeout=timeout)
        return response.content

