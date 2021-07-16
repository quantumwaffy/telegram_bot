import logging
import os
from threading import Thread
from time import sleep

import requests
from bs4 import BeautifulSoup
from flask import Flask

app = Flask("")

WORK_DIR = os.getcwd()
CACHE_DIR = "cache_files"
SOURCE = "https://myfin.by/currency/"

CITIES = {
    "1": ("minsk", "Минск"),
    "2": ("brest", "Брест"),
    "3": ("vitebsk", "Витебск"),
    "4": ("gomel", "Гомель"),
    "5": ("grodno", "Гродно"),
    "6": ("mogilev", "Могилев"),
}


@app.route("/")
def home():
    return "Hello, I am alive!"


def run():
    app.run(host="0.0.0.0", port=8080)


def make_keep_alive():
    logging.basicConfig(level=logging.DEBUG)
    s = requests.Session()
    r = s.get("http://httpbin.org/cookies")
    print(r.text)
    t = Thread(target=run)
    t.start()


def update_cache_files():
    cache_path = os.path.join(WORK_DIR, CACHE_DIR)
    cache_files = os.listdir(cache_path)
    if os.path.exists(cache_path) and cache_files:
        for file in os.listdir(cache_path):
            os.remove(os.path.join(WORK_DIR, CACHE_DIR, file))
    if os.path.exists(cache_path) and not cache_files:
        for name in CITIES.values():
            url = SOURCE + name[0]
            file = os.path.join(WORK_DIR, CACHE_DIR, "temporary_" + name[0] + ".html")
            response = requests.get(url, headers={"User-agent": "your bot 0.1"})
            with open(file, "w") as f:
                f.write(str(BeautifulSoup(response.text, "lxml")))
            sleep(1)
        sleep(1800)
        update_cache_files()
