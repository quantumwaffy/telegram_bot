from datetime import datetime

import pyowm
import telebot
from pyowm.commons import exceptions as exc
from pyowm.utils.config import get_default_config

from keep_alive import make_keep_alive
from local_tokens import pyowm_token, telegram_token

bot = telebot.TeleBot(telegram_token)
print("Connected with Telegram")
config_dict = get_default_config()
config_dict["language"] = "ru"
owm = pyowm.OWM(pyowm_token, config_dict)
print("Connected with PYOWM")


def inf(message):
    now = datetime.strftime(datetime.now(), "%d.%m.%Y/%H:%M:%S")
    userid = message.chat.id
    name = message.chat.first_name
    sname = message.chat.last_name
    text = message.text
    with open("log.txt", "a") as f:
        f.write("Time: %s. Name: %s %s. ID: %i. Text: %s\n" % (now, name, sname, userid, text))


@bot.message_handler(commands=["start"])
def welcome(message):
    with open("AnimatedSticker.tgs", "rb") as f:
        bot.send_sticker(message.chat.id, f)
        bot.send_message(
            message.chat.id,
            f"Привет, <b>{message.from_user.first_name}</b>!\nЯ <b>{bot.get_me().first_name}"
            f"</b>, бот, который еще в процессе разработки!\nВведи название города, и я подскажу погоду на сегодня: ",
            parse_mode="html",
        )
        inf(message)


@bot.message_handler(content_types=["text"])
def send(message):
    try:
        city = message.text
        inf(message)
        obs = owm.weather_manager().weather_at_place(city)
        weather = obs.weather
        temp = round(weather.temperature("celsius")["temp"])
        wind = weather.wind()["speed"]
        bot.send_message(
            message.chat.id,
            "В городе "
            + city
            + " сейчас "
            + weather.detailed_status
            + ".\nТемпература в районе "
            + str(temp)
            + " ℃.\nСкорость ветра составляет "
            + str(wind)
            + " м/с.",
        )
        if temp < 3:
            bot.send_message(message.chat.id, "Надень одежду потеплее, на улице холодно")
        elif temp >= 3 and temp < 20:
            bot.send_message(message.chat.id, "Температура нормальная, но куртку надеть надо")
        else:
            bot.send_message(message.chat.id, "Шорты и вперед")

    except exc.APIResponseError:
        bot.send_message(message.chat.id, "Такого города не существует.")
        inf(message)


print("Running")
make_keep_alive()
bot.polling(none_stop=True)
