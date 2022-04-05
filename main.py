import os
from urllib.parse import urlparse

import requests
from dotenv import dotenv_values


CUSTOM_DOMAIN = dotenv_values(".env").get("CUSTOM_DOMAIN","")

BITLY_TOKEN = dotenv_values(".env")["BITLY_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {BITLY_TOKEN}"
}


def shorten_link(url):
    payload = {"long_url": url,
                "domain": CUSTOM_DOMAIN}

    response = requests.post("https://api-ssl.bitly.com/v4/shorten",
                             headers=HEADERS,
                             json=payload)

    response.raise_for_status()

    return response.json()["id"]


def count_number_clicks(bitlink):
    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/"\
                            f"{bitlink}/clicks/summary",
                            headers=HEADERS)

    response.raise_for_status()

    return response.json()["total_clicks"]


def is_bitlink(bitlink):
    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}",
                            headers=HEADERS)

    return response.ok


def checking_existence(url):
    response = requests.get(url)

    response.raise_for_status()


if __name__ == "__main__":
    url = input()

    parsed_link = urlparse(url)
    url_without_protocol = f"{parsed_link.netloc}{parsed_link.path}"

    try:
        checking_existence(url)
        if is_bitlink(url_without_protocol):
            try:
                print(count_number_clicks(url_without_protocol))
            except requests.exceptions.HTTPError as error:
                exit("Ошибка:\n{0}".format(error))
        else:
            try:
                print(shorten_link(url))
            except requests.exceptions.HTTPError as error:
                exit("Ошибка, неверная ссылка:\n{0}".format(error))
    except requests.exceptions.HTTPError as error:
        exit("Ссылка не существует:\n{0}".format(error))
