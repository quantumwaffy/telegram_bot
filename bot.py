import telebot
import pyowm
from datetime import datetime

from pyowm.utils.config import get_default_config
from pyowm.commons import exceptions as exc

bot = telebot.TeleBot('1028964503:AAHnmXie45UuSSdPzOk8WwWDo6JQojuCOVo')
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = pyowm.OWM('1ee6c77753006e90884a66184101b7b4', config_dict)


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
	stick = open ('files\AnimatedSticker.tgs','rb')
	bot.send_sticker (message.chat.id, stick)
	bot.send_message (message.chat.id, "Дарова, <b>{0.first_name}</b>!\nЯ <b>{1.first_name}</b>, бот, который еще разрабатывается!\nВведи название города, и я подскажу погоду на сегодня: ".format(message.from_user,bot.get_me()),parse_mode ="html" )
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
			bot.send_message (message.chat.id, "Надень одежду потеплее, на улице макимально холодно, шо охереть")
		elif (temp>=3 and temp<20) :
			bot.send_message (message.chat.id, "Ну температура пойдет, но куртку надеть надо")
		else :
			bot.send_message (message.chat.id, "Шорты и погнал")

	except exc.APIResponseError:
		bot.send_message (message.chat.id, "Такого города не существует.")
		inf(message)
bot.polling(none_stop = True)
