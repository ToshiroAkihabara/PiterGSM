import requests
import json
import os

from tqdm import tqdm
from bs4 import BeautifulSoup as BS
from time import sleep
from decorator import time_of_working as times
from config import headers


def catalogs() -> json:
    """Save links of catalogs and numbers of pages in json"""
    """Сохраняет ссылки на каталоги и количество страниц в json"""

    try:
        os.mkdir("json_files")
        url = "https://pitergsm.ru/catalog/"
        response = requests.get(url=url, headers=headers)
        soup = BS(response.text, "lxml")
        catalogs_href = soup.find_all("div", class_="catalog__item")
        catalog_list = []
        for catalog in tqdm(catalogs_href):
            catalog_href = catalog.get("href")
            catalog_list.append(catalog_href)
        dict = {}
        for catalog in tqdm(catalog_list):
            for catalog_name, last_page in pagination(catalog):
                dict[catalog_name] = last_page

        with open("json_files/catalogs.json", "w", encoding="utf-8") as file:
            json.dump(dict, file, indent=4, ensure_ascii=False)

    except KeyboardInterrupt as e:
        print("Принудительное завершение скрипта!")
        raise (e)

    except FileExistsError:
        with open("json_files/catalogs.json", "w", encoding="utf-8") as file:
            json.dump(dict, file, indent=4, ensure_ascii=False)


def pagination(catalog: str) -> dict:
    """Parse links and numbers of pages"""
    """Получение ссылок и количество страниц"""

    try:
        count = 1
        while True:
            url = f"https://pitergsm.ru{catalog}?PAGEN_1={count}"
            responce = requests.get(url=url, headers=headers)
            soup = BS(responce.text, "lxml")
            pagination_next = soup.find("div", class_="page-paging").find(
                "a", class_="paging__next"
            )
            if pagination_next:
                count += 1
                sleep(0.1)
            else:
                last_page = count
                catalog_name = catalog
                yield catalog_name, last_page
                break

    except AttributeError:
        last_page = count
        catalog_name = catalog
        yield catalog_name, last_page

    except KeyboardInterrupt as e:
        print("Принудительное завершение скрипта!")
        raise (e)


@times
def main() -> json:
    """Create the massive of data in json"""
    """Создание массива данных в json"""

    try:
        with open("json_files/catalogs.json", encoding="utf-8") as file:
            dict_json = json.load(file)
        massive = {}
        for key, value in tqdm(dict_json.items()):
            catalog = key.split("/")[-2]
            links = []
            for count in range(1, value + 1):
                url = f"https://pitergsm.ru{key}?PAGEN_1={count}"
                links.append(url)
            massive[catalog] = links

        with open("json_files/pagination.json", "w", encoding="utf-8") as file:
            json.dump(massive, file, indent=4, ensure_ascii=False)

    except FileNotFoundError:
        catalogs()

    except KeyboardInterrupt as e:
        print("Принудительное завершение скрипта!")
        raise (e)


if __name__ == "__main__":
    main()
