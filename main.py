import telebot
import pyowm
from datetime import datetime
from keep_alive import make_keep_alive
from pyowm.utils.config import get_default_config
from pyowm.commons import exceptions as exc

try:
	from .local_tokens import *
	tel_token = telegram_token
	owm_token = pyowm_token
except ImportError:
	from tokens import *
	tel_token = telegram_token
	owm_token = pyowm_token

bot = telebot.TeleBot(tel_token)
print("Connected with Telegram")
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = pyowm.OWM(pyowm_token, config_dict)
print("Connected with PYOWM")


def inf (message):
	now = datetime.strftime(datetime.now(), "%d.%m.%Y/%H:%M:%S")
	userid = message.chat.id
	name = message.chat.first_name
	sname = message.chat.last_name
	text = message.text
	file = open('log.txt', 'a')
	file.write("Time: %s. Name: %s %s. ID: %i. Text: %s\n" %(now, name, sname, userid,text))
	file.close()

@bot.message_handler(commands=['start'])
def welcome(message):
	stick = open ('AnimatedSticker.tgs','rb')
	bot.send_sticker (message.chat.id, stick)
	bot.send_message (message.chat.id, "Привет, <b>{0.first_name}</b>!\nЯ <b>{1.first_name}</b>, бот, который еще в процессе разработки!\nВведи название города, и я подскажу погоду на сегодня: ".format(message.from_user,bot.get_me()),parse_mode ="html" )
	inf(message)

@bot.message_handler(content_types=['text'])
def send (message):
	try:
		city = message.text
		inf(message)
		obs = owm.weather_manager().weather_at_place(city)
		weather = obs.weather
		temp = round(weather.temperature('celsius')['temp'])
		wind = weather.wind()['speed']
		bot.send_message (message.chat.id, "В городе "+ city + " сейчас " + weather.detailed_status + ".\nТемпература в районе "+str(temp)+" ℃.\nСкорость ветра составляет "+ str(wind)+" м/с.")
		if temp<3:
			bot.send_message (message.chat.id, "Надень одежду потеплее, на улице холодно")
		elif (temp>=3 and temp<20) :
			bot.send_message (message.chat.id, "Температура нормальная, но куртку надеть надо")
		else :
			bot.send_message (message.chat.id, "Шорты и вперед")

	except exc.APIResponseError:
		bot.send_message (message.chat.id, "Такого города не существует.")
		inf(message)
print("Running")
make_keep_alive()
bot.polling(none_stop = True)



