import csv
import pandas
import re
import os
import requests
import struct
import urllib.request

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def requests_test():
    img_url = "http://livedoor.blogimg.jp/anico_bin/imgs/3/4/34073d32.jpg"
    response = requests.get(img_url, allow_redirects=True, timeout=10)
    print(response.status_code)
    img = response.content
    with open("./cap/file.jpg", "wb") as file:
        file.write(img)

def csv_test():
    csv_dir = os.path.join(PROJECT_DIR, "datas/2017_winter.csv")
    csv = pandas.read_csv(csv_dir)
    for column in csv.columns.values.tolist():
        values = csv[column].tolist()
        for value in values:
            print(value)
            if value != value:
                print("aaaa")

    # with open('test.csv', 'r') as f:
    #     reader = csv.reader(f)
    #     header = next(reader)
    #
    #     for row in reader:
    #         print(row)

def img_size_test():
    def get_image_size(url):
        response = urllib.request.urlopen(url)
        size = (-1, -1)
        if response.status == 200:
            signature = response.read(2)
            if signature == b'\xff\xd8':  # jpg
                size = parse_jpeg(response)
            elif signature == b'\x89\x50':  # png
                size = parse_png(response)
            elif signature == b'\x47\x49':  # gif
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

    url = "http://livedoor.blogimg.jp/anico_bin/imgs/3/4/34073d32.jpg"
    size=get_image_size(url)
    print(size[0])

def re_test():
    pattern = r"http://livedoor.blogimg.jp/anico_bin/imgs/.*-s.(jpg|png|gif)"
    text = "http://livedoor.blogimg.jp/anico_bin/imgs/0/0/0005d297-s.jpg"
    worng = "http://resize.blogsys.jp/e195df337a76bde8db84ca2cca2166a33dfdee1f/crop1/80x70/http://livedoor.blogimg.jp/anico_bin/imgs/b/5/b5f51dcf.jpg"
    result1 = len(re.findall(pattern, text))>0
    result2 = len(re.findall(pattern, worng))>0
    print(result1)
    print(result2)
    ext = os.path.splitext(text)[1]

    if ext == ".jpg":
        text = text.replace('-s.jpg', '.jpg')
    elif ext == ".png":
        text = text.replace('-s.png', '.png')

csv_test()
