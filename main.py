import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import dotenv_values


CUSTOM_DOMAIN = dotenv_values(".env").get("CUSTOM_DOMAIN", "")

BITLY_TOKEN = dotenv_values(".env")["BITLY_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {BITLY_TOKEN}"
}

MAIN_LINK = "https://api-ssl.bitly.com/v4/"


def shorten_link(url):
    payload = {
        "long_url": url,
        "domain": CUSTOM_DOMAIN
    }

    response = requests.post(
        f"{MAIN_LINK}shorten",
        headers=HEADERS,
        json=payload
    )

    response.raise_for_status()

    return response.json()["id"]


def count_number_clicks(bitlink):
    response = requests.get(
        f"{MAIN_LINK}bitlinks/"\
        f"{bitlink}/clicks/summary",
        headers=HEADERS
    )

    response.raise_for_status()

    return response.json()["total_clicks"]


def is_bitlink(bitlink):
    response = requests.get(
        f"{MAIN_LINK}bitlinks/{bitlink}",
        headers=HEADERS
    )

    return response.ok


def checking_existence(url):
    response = requests.get(f"http://{url}")

    response.raise_for_status()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Программа считает ссылки и сокращает их'
    )

    parser.add_argument('link', help='Подставьте ссылку сюда')

    args = parser.parse_args()

    url = args.link

    parsed_link = urlparse(url)
    url_without_protocol = f"{parsed_link.netloc}{parsed_link.path}"

    try:
        checking_existence(url_without_protocol)
        if is_bitlink(url_without_protocol):
            print(count_number_clicks(url_without_protocol))
        else:
            print(shorten_link(url))
    except requests.exceptions.HTTPError as error:
        exit("Ссылка не существует или произошла ошибка:\n{0}".format(error))
