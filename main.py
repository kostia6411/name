import os

import requests
from dotenv import load_dotenv, dotenv_values
from urllib.parse import urlparse


BITLY_TOKEN = dotenv_values(".env")["BITLY_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {BITLY_TOKEN}"
}


def shorten_link(url):
    long_url = {"long_url": url}

    response = requests.post("https://api-ssl.bitly.com/v4/shorten",
                             headers=HEADERS,
                             json=long_url)

    response.raise_for_status()

    return response.json()["id"]


def count_number_clicks(bitlink):
    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/"
                            "{bitlink}/clicks/summary",
                            headers=HEADERS)

    response.raise_for_status()

    return response.json()["total_clicks"]


def is_bitlink(bitlink):
    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}",
                            headers=HEADERS)

    return response.ok


if __name__ == "__main__":
    load_dotenv()

    url = input()

    parts_link = urlparse(url)
    glued_link = f"{parts_link.netloc}{parts_link.path}"

    if is_bitlink(glued_link):
        try:
            print(count_number_clicks(glued_link))
        except requests.exceptions.HTTPError:
            print("Ошибка")
    else:
        try:
            print(shorten_link(url))
        except requests.exceptions.HTTPError:
            print("Ошибка, неверная ссылка")
