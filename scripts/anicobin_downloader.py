import os
import re
import pandas
from scripts.image import Image

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


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


def make_filename(anime, story_no, img_index, img_url):
    anime_dir = os.path.join(PROJECT_DIR, "cap/%s" % anime)
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


def main():
    print("dataフォルダの中のcsvファイルの名前を入力(拡張子も一緒に)")
    csv_name = input()
    csv_dir = os.path.join(PROJECT_DIR, "datas/" + csv_name)
    if not os.path.exists(csv_dir):
        print("csvファイルがないぞ！")
        return
    csv = pandas.read_csv(csv_dir)

    for anime in csv.columns.values.tolist():
        url_array = csv[anime].tolist()
        story_no = 1
        for url in url_array:
            if url != url:
                print("this is nan row!!")
                break
            img_url_array = Image.get_img_url(url)
            img_index = 1
            for img_url in img_url_array:
                if check_img_type(img_url):
                    img_url = remake_img_url(img_url)
                    image = Image.download(img_url)
                    file_name = make_filename(anime, story_no, img_index, img_url)
                    Image.save(image, file_name)
                    img_index += 1
            story_no += 1

if __name__ == "__main__":
    main()
