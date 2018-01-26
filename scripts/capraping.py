import re
import requests
from bs4 import BeautifulSoup
from scripts.image import Image
from scripts.anicobin import Anicobin
from scripts.web_request import WebRequest

print("ダウンロードする画像サイズの下限を入力(x,y)")
x, y = input().split(",")
x, y = int(x), int(y)
if x < 0 or y < 0:
    print("0以上を入力せんかい")
    quit

for i in range(1, 10):
    root_url = "http://anicobin.ldblog.jp/?p="+str(i)
    response = requests.get(root_url, allow_redirects=True, timeout=10)
    soup = BeautifulSoup(response.text)
    anime_urls = soup.find_all("h2", class_='top-article-title')
    for anime in anime_urls:
        anime_url = anime.a.get("href")

        response = requests.get(anime_url, allow_redirects=True, timeout=10)
        soup = BeautifulSoup(response.text)
        img_url_array = [link.get('src') for link in soup.find_all('img')]

        title = soup.find("h1", class_="article-title").string
        anime_title = re.search(r"【(?P<name>.*)】", title).group("name")
        story_no = re.search(r"第(?P<no>.*)話", title).group("no")

        img_index = 1
        for img_url in img_url_array:
            is_cap = Anicobin.check_img_type(img_url)
            if not is_cap:
                # print("this is not cap image")
                continue
            image_size = WebRequest.get_img_size(img_url)
            if image_size[0] > x and image_size[1] > y:
                img_url = Anicobin.remake_img_url(img_url)
                image = WebRequest.download(img_url)
                file_name = Image.make_filename(anime_title, story_no, img_index, img_url)
                print(file_name)
                Image.save(image, file_name)
                img_index += 1
