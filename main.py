from dotenv import load_dotenv
import requests
import os


def shorten_link(token, url):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    long_url = {"long_url":url}

    response = requests.post("https://api-ssl.bitly.com/v4/shorten", headers=headers,json=long_url)

    response.raise_for_status()

    return response.json()["id"]

def click_count(token, bitlink):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary", headers=headers)

    response.raise_for_status()

    return response.json()["total_clicks"]


def is_bitlink(token, bitlink):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}", headers=headers)

    return response.ok

if __name__ == "__main__":
    load_dotenv()

    token = os.getenv('TOKEN')

    url = input()

    if is_bitlink(token, url) == True:

        try:
            print(click_count(token, url))
        except requests.exceptions.HTTPError:
            print("Ошибка")
    else:
        try:
            print(shorten_link(token, url))
        except requests.exceptions.HTTPError:
            print("Ошибка, неверная ссылка")

    """bit.ly/3fa6jy6 = "http://dvmn.org/modules/web-api/lesson/bitly/#3"""
