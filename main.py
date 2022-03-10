from urllib.parse import urlparse
from dotenv import load_dotenv
import requests
import os


def shorten_link(bitly_token, url):
    headers = {
        "Authorization": f"Bearer {bitly_token}"
    }

    long_url = {"long_url":url}

    response = requests.post("https://api-ssl.bitly.com/v4/shorten", headers=headers,json=long_url)

    response.raise_for_status()

    return response.json()["id"]

def count_number_clicks(token, bitlink):
    headers = {
        "Authorization": f"Bearer {bitly_token}"
    }

    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary", headers=headers)

    response.raise_for_status()

    return response.json()["total_clicks"]


def is_bitlink(bitly_token, bitlink):
    headers = {
        "Authorization": f"Bearer {bitly_token}"
    }

    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}", headers=headers)

    return response.ok

if __name__ == "__main__":
    load_dotenv()

    bitly_token = os.getenv('BITLY_TOKEN')

    url = input()

    parts_link = urlparse(url)
    glued_link = f"{parts_link.netloc}{parts_link.path}"

    if is_bitlink(bitly_token, glued_link) == True:
        try:
            print(count_number_clicks(bitly_token, glued_link))
        except requests.exceptions.HTTPError:
            print("Ошибка")
    else:
        try:
            print(shorten_link(bitly_token, url))
        except requests.exceptions.HTTPError:
            print("Ошибка, неверная ссылка")

    """bit.ly/3fa6jy6 = "http://dvmn.org/modules/web-api/lesson/bitly/#3"""
