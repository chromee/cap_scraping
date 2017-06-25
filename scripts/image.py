from bs4 import BeautifulSoup
import requests
import urllib.request
import struct


class Image:

    @staticmethod
    def get_img_url(html_url, timeout=10):
        response = requests.get(html_url, allow_redirects=True, timeout=timeout)
        soup = BeautifulSoup(response.text)
        img_url_array = [link.get('src') for link in soup.find_all('img')]
        return img_url_array

    @staticmethod
    def get_size(url):
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
    def parse_jpeg(response):
        while not response.closed:
            (marker, size) = struct.unpack('>2sH', response.read(4))
            if marker == b'\xff\xc0':
                (_, height, width, _) = struct.unpack('>chh10s', response.read(size - 2))
                return width, height
            else:
                response.read(size - 2)

    @staticmethod
    def parse_png(response):
        (_, width, height) = struct.unpack(">14sII", response.read(22))
        return width, height

    @staticmethod
    def parse_gif(response):
        (_, width, height) = struct.unpack("<4sHH", response.read(8))
        return width, height

    @staticmethod
    def download(img_url, timeout=10):
        response = requests.get(img_url, allow_redirects=True, timeout=timeout)
        return response.content

    @staticmethod
    def save(image, file_name):
        with open(file_name, "wb") as file:
            file.write(image)
