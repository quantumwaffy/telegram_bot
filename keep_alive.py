from flask import Flask
from threading import Thread
import logging
import requests

app = Flask('')


@app.route('/')
def home():
  return "Hello, I am alive!"


def run():
  app.run(host='0.0.0.0', port=8080)


def make_keep_alive():
  logging.basicConfig(level=logging.DEBUG)
  s = requests.Session()
  r = s.get("http://httpbin.org/cookies")
  print(r.text)
  t = Thread(target=run)
  t.start()