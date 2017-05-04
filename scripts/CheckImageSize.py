import struct
import urllib


class CheckImageSize:

    @staticmethod
    def get_image_size(url):
        response = urllib.request.urlopen(url)
        size = (-1,-1)
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
    return width, height