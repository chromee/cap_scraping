import os
import pandas
from scripts.image import Image

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

    print("ダウンロードする画像サイズの下限を入力(x,y)")
    x, y = int(input().split(","))
    x, y = int(x), int(y)
    if x < 0 or y < 0:
        print("0以上を入力せんかい")
        return
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
                    image_size = Image.get_size(img_url)
                    if image_size[0] > x and image_size[1] > y:
                        image = Image.download(img_url)
                        file_name = Image.make_filename(csv_dir, anime, story_no, img_index, img_url)
                        Image.save(image, file_name)
                        img_index += 1

if __name__ == "__main__":
    main()
