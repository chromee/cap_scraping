import os
import pandas
import requests
from scripts.image import Image
from scripts.anicobin import Anicobin

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def main():
    print("dataフォルダの中のcsvファイルの名前を入力(拡張子も一緒に)")
    input_str = input()
    csv_names = input_str.split()

    for csv_name in csv_names:
        csv_dir = os.path.join(PROJECT_DIR, "data/" + csv_name)
        if not os.path.exists(csv_dir):
            print("%sなんてないぞ！" % csv_dir)
            csv_names.remove(csv_name)

    for csv_name in csv_names:
        csv_dir = os.path.join(PROJECT_DIR, "data/" + csv_name)
        csv = pandas.read_csv(csv_dir)
        for anime in csv.columns.values.tolist():
            url_array = csv[anime].tolist()
            story_no = 0
            for url in url_array:
                story_no += 1
                if url != url:
                    print("this is nan row!!")
                    break
                img_url_array = Image.get_img_url(url)
                img_index = 1
                for img_url in img_url_array:
                    is_cap = Anicobin.check_img_type(img_url)
                    if not is_cap:
                        print("this is not cap image")
                        continue
                    try:
                        img_url = Anicobin.remake_img_url(img_url)
                        print(img_url)
                        image = Image.download(img_url)
                        file_name = Image.make_filename(csv_name, anime, story_no, img_index, img_url)
                        Image.save(image, file_name)
                        img_index += 1
                    except requests.exceptions.RequestException as e:
                        print(e)
                        continue


if __name__ == "__main__":
    main()
