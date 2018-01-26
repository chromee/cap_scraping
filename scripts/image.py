import struct
import os

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


class Image:
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
    def make_filename(anime, story_no, img_index, img_url):
        anime_dir = os.path.join(PROJECT_DIR, "cap\%s" % anime)
        if not os.path.exists(anime_dir):
            os.mkdir(anime_dir)
        base_dir = os.path.join(anime_dir, "%s_%s話" % (anime, story_no))
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        title = "%s_%s_%s" % (anime, story_no, img_index)
        ext = os.path.splitext(img_url)[1]
        file_name = title + ext
        full_path = os.path.join(base_dir, file_name)
        return full_path

    @staticmethod
    def save(image, file_name):
        with open(file_name, "wb") as file:
            file.write(image)
