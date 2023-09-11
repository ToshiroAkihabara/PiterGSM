import requests
import json
import csv
import os
import random
import pagination as pagination

from bs4 import BeautifulSoup as BS
from time import sleep
from decorator import time_of_working as times
from config import headers


def parse_html(count: int, key: str) -> list:
    """Parse and insert datas from html into early created csv files and return massive with data"""
    """Извлекает данные из html страниц и вставляет их в csv файлы, затем возвращает массив данных"""

    try:
        with open(f"data_html/{count}_{key}.html", encoding="utf-8") as file:
            scr = file.read()

        soup = BS(scr, "lxml")
        data = soup.find_all("div", class_="catalog__list like-cards")
        all_data = []
        for i in data:
            cards = i.find_all("div", class_="catalog__item")
            for card in cards:
                data_dict = {}
                try:
                    title = card.find("div", class_="prod-card__title").text
                    available = card.find(
                        "div", class_="prod-card__count icon-check-green nodesktop"
                    ).text
                    if not available:
                        raise AttributeError("Нет в наличии")
                    price = (
                        card.find("div", class_="price__now")
                        .text.replace("a", " ")
                        .strip()
                    )
                    url_page = "https://pitergsm.ru" + card.find(
                        "div", class_="prod-card"
                    ).find("a", class_="prod-card__link").get("href")
                    data_dict[key] = title, available, price, url_page

                    with open(f"csv_files/{key}.csv", "a", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow((title, available, price, url_page))
                    all_data.append(data_dict)
                except AttributeError:
                    available = "Нет в наличии"

        yield all_data

    except KeyboardInterrupt as e:
        print("Принудительное завершение скрипта!")
        raise (e)


def create_csv() -> csv:
    """"Create the csv table of every catalogs with names of columns"""
    """Создает csv таблицу под каждый каталог и задает названия столбцам"""

    try:
        with open("json_files/pagination.json", encoding="utf-8") as file:
            massive = json.load(file)
        try:
            os.mkdir("csv_files")
            for key, value in massive.items():
                with open(f"csv_files/{key}.csv", "w", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (
                            "Наименование",
                            "Доступность",
                            "Стоимость в рублях",
                            "Ссылка на карточку",
                        )
                    )
        except FileExistsError:
            for key, value in massive.items():
                with open(f"csv_files/{key}.csv", "w", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (
                            "Наименование",
                            "Доступность",
                            "Стоимость в рублях",
                            "Ссылка на карточку",
                        )
                    )

    except KeyboardInterrupt as e:
        print("Принудительное завершение скрипта!")
        raise (e)


def create_json() -> json:
    """Save the data with html and extraction the massive of data in json"""
    """Сохраняет данные html страниц с последующим извлечение массива данных в json файл"""

    try:
        create_csv()
        with open("json_files/pagination.json", encoding="utf-8") as file:
            massive = json.load(file)

        try:
            os.mkdir("data_html")
            count = 0
            json_dump = []
            for key, value in massive.items():
                for url in value:
                    response = requests.get(url=url, headers=headers)
                    scr = response.text
                    with open(
                        f"data_html/{count}_{key}.html", "w", encoding="utf-8"
                    ) as file:
                        file.write(scr)
                    parse_html(count, key)
                    for data in parse_html(count, key):
                        json_dump.append(data)
                    sleep(random.randrange(2, 3))
                    os.remove(f"data_html/{count}_{key}.html")
                    count += 1
            with open("json_files/piterGSM.json", "a", encoding="utf-8") as f:
                json.dump(json_dump, f, indent=4, ensure_ascii=False)

        except FileExistsError:
            count = 0
            json_dump = []
            for key, value in massive.items():
                for url in value:
                    response = requests.get(url=url, headers=headers)
                    scr = response.text
                    with open(
                        f"data_html/{count}_{key}.html", "w", encoding="utf-8"
                    ) as file:
                        file.write(scr)
                    parse_html(count, key)
                    for data in parse_html(count, key):
                        json_dump.append(data)
                    sleep(random.randrange(2, 3))
                    os.remove(f"data_html/{count}_{key}.html")
                    count += 1
            with open("json_files/piterGSM.json", "a", encoding="utf-8") as f:
                json.dump(json_dump, f, indent=4, ensure_ascii=False)

    except KeyboardInterrupt as e:
        print("Принудительное завершение скрипта!")
        os.remove(f"data/{count}_{key}.html")
        raise (e)


@times
def main() -> None:
    """Get json and csv files"""
    """Получает json и csv файлы"""

    try:
        create_json()

    except FileNotFoundError:
        pagination.main()
        sleep(2)
        main()

    except KeyboardInterrupt as e:
        print("Принудительное завершение скрипта!")
        raise (e)


if __name__ == "__main__":
    main()
