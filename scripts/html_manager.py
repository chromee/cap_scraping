import difflib
from bs4 import BeautifulSoup


class HtmlManager:
    html = ""

    @staticmethod
    def get_diff(new_html, update=True):
        diff = difflib.HtmlDiff()
        html_table = diff.make_file([HtmlManager.html], [new_html])
        if update:
            HtmlManager.html = new_html
        return html_table

    @staticmethod
    def extract_img_urls(source=html):
        soup = BeautifulSoup(source)
        img_url_array = [link.get('src') for link in soup.find_all('img')]
        return img_url_array
