from datetime import datetime

import pyowm
from keyboa.keyboards import keyboa_maker
from pyowm.commons import exceptions as exc
from pyowm.utils.config import get_default_config
from telebot import TeleBot

from keep_alive import make_keep_alive
from local_tokens import pyowm_token, telegram_token
from utils.parser import CITIES, make_soup, parsing_soup, user_input

bot = TeleBot(telegram_token)
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
        f"</b> - бот, который еще в процессе разработки...",
        parse_mode="html",
    )
    inf(message)


@bot.message_handler(commands=["weather"])
def send(message):
    bot.send_message(
        message.chat.id,
        "Введи название города, и я подскажу погоду на сегодня: ",
    )

    @bot.message_handler(content_types=["text"])
    def get_weather(message):
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


@bot.message_handler(commands=["banks"])
def currencies_information(message):
    cities = [{text[1]: ident} for ident, text in CITIES.items()]
    kb_cities = keyboa_maker(items=cities, items_in_row=3)
    bot.send_message(
        message.chat.id,
        reply_markup=kb_cities,
        text="Выбери город РБ, я поищу акутальные курсы обмена валют на сегодня: ",
    )
    result_list = []

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        choices = [
            {"Узнать все курсы валют": "c1"},
            {"Узнать банки с лучшим курсом валют": "c2"},
            {"Узнать лучший курс покупки $": "c3"},
            {"Узнать лучший курс продажи $": "c4"},
            {"Узнать лучший курс покупки €": "c5"},
            {"Узнать лучший курс продажи €": "c6"},
            {"Узнать лучший курс покупки ₽": "c7"},
            {"Узнать лучший курс продажи ₽": "c8"},
            {"Узнать лучший курс покупки $ c €": "c9"},
            {"Узнать лучший курс продажи $ c €": "c10"},
        ]
        if "c" not in call.data:
            file = make_soup(call.data)
            list_dicts = parsing_soup(file)
            result_list.extend(list_dicts)

            if list_dicts:
                kb_choices = keyboa_maker(items=choices, items_in_row=1)
                bot.send_message(
                    message.chat.id,
                    reply_markup=kb_choices,
                    text="Выбери то, что ты хочешь узнать: ",
                )
        else:
            chosen_dict_info = user_input(call.data, result_list)
            text_message = (
                "".join(text for el in choices for text, ident in el.items() if ident == call.data)
                .split("Узнать ")[1]
                .upper()
                + ":\n"
            )
            for bank, currencies in chosen_dict_info.items():
                text_message += "\n" + bank + ":\n"
                for kind, value in currencies.items():
                    text_message += kind + ": " + value + "\n"

            bot.send_message(message.chat.id, text=text_message)


print("Running")
make_keep_alive()
bot.polling(none_stop=True)
