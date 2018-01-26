import os
import re


class Anicobin:
    @staticmethod
    def check_img_type(img_url):
        pattern = r"http://livedoor.blogimg.jp/anico_bin/imgs/.*-s.(jpg|png|gif)"
        anti_pattern = r"http://resize.blogsys.jp/.*/" + pattern
        result = len(re.findall(pattern, img_url)) > 0
        anti_result = len(re.findall(anti_pattern, img_url)) > 0
        return result and not anti_result

    @staticmethod
    def remake_img_url(img_url):
        remaked_url = ""
        ext = os.path.splitext(img_url)[1]
        if ext == ".jpg":
            remaked_url = img_url.replace('-s.jpg', '.jpg')
        elif ext == ".png":
            remaked_url = img_url.replace('-s.png', '.png')
        return remaked_url
