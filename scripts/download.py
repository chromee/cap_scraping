import os
import re
import pandas
import requests
import struct
import urllib.request
from bs4 import BeautifulSoup

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def get_img_url(html_url, timeout=10):
    response = requests.get(html_url, allow_redirects=True, timeout=timeout)
    soup = BeautifulSoup(response.text)
    img_url_array = [link.get('src') for link in soup.find_all('img')]
    return img_url_array


def check_img_type(img_url):
    pattern = r"http://livedoor.blogimg.jp/anico_bin/imgs/.*-s.(jpg|png|gif)"
    anti_pattern = r"http://resize.blogsys.jp/.*/" + pattern
    result = len(re.findall(pattern, img_url)) > 0
    anti_result = len(re.findall(anti_pattern, img_url)) > 0
    return result and not anti_result


def remake_img_url(img_url):
    remaked_url = ""
    ext = os.path.splitext(img_url)[1]
    if ext == ".jpg":
        remaked_url = img_url.replace('-s.jpg', '.jpg')
    elif ext == ".png":
        remaked_url = img_url.replace('-s.png', '.png')
    return remaked_url


def download_image(img_url, timeout=10):
    response = requests.get(img_url, allow_redirects=True, timeout=timeout)
    return response.content


def make_filename(anime, anime_no, img_index, img_url):
    anime_dir = os.path.join(PROJECT_DIR, "cap/%s" % anime)
    if not os.path.exists(anime_dir):
        os.mkdir(anime_dir)
    base_dir = os.path.join(anime_dir, "%s_%s話" % (anime, anime_no))
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    title = "%s_%s_%s" % (anime, anime_no, img_index)
    ext = os.path.splitext(img_url)[1]
    file_name = title + ext
    full_path = os.path.join(base_dir, file_name)
    return full_path


def save_image(file_name, image):
    with open(file_name, "wb") as file:
        file.write(image)


def get_image_size(url):
    response = urllib.request.urlopen(url)
    size = (-1, -1)
    if response.status == 200:
        signature = response.read(2)
        if signature == b'\xff\xd8': #jpg
            size = parse_jpeg(response)
        elif signature == b'\x89\x50': #png
            size = parse_png(response)
        elif signature == b'\x47\x49': #gif
            size = parse_gif(response)
    response.close()
    return size


def parse_jpeg(response):
    while not response.closed:
        (marker, size) = struct.unpack('>2sH', response.read(4))
        if marker == b'\xff\xc0':
            (_, height, width, _) = struct.unpack('>chh10s', response.read(size - 2))
            return width, height
        else:
            response.read(size - 2)


def parse_png(response):
    (_, width, height) = struct.unpack(">14sII", response.read(22))
    return width, height


def parse_gif(response):
    (_, width, height) = struct.unpack("<4sHH", response.read(8))
    return width,


if __name__ == "__main__":
    csv_dir = os.path.join(PROJECT_DIR, "datas/2016_fall.csv")
    csv = pandas.read_csv(csv_dir)
    for anime in csv.columns.values.tolist():
        html_url_array = csv[anime].tolist()
        anime_no = 0
        for html_url in html_url_array:
            anime_no += 1
            if html_url != html_url:    #NaN回避
                print("NaN html_url")
                continue
            img_url_array = get_img_url(html_url)
            img_index = 1
            for img_url in img_url_array:
                is_cap = check_img_type(img_url)
                if not is_cap:
                    print("not cap image")
                    continue
                try:
                    img_url = remake_img_url(img_url)
                    print(img_url)
                    image = download_image(img_url)
                    file_name = make_filename(anime, anime_no, img_index, img_url)
                    save_image(file_name, image)
                    img_index += 1
                except requests.exceptions.RequestException as e:
                    print(e)

