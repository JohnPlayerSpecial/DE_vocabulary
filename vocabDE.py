from bs4 import BeautifulSoup
from random import randint
import telegram
from telegram.error import Unauthorized, NetworkError
from telegram.ext import *
import datetime
import time
from textblob import TextBlob
from random import shuffle
from urllib.request import urlopen
import os

HOUR_I_WANNA_GET_MESSAGE = int( os.environ['hour'] )
MINUTES_I_WANNA_GET_MESSAGE = int( os.environ['minute'] )

html = urlopen('http://slowgerman.com/vokabeln/').read()
bsObj = BeautifulSoup(html,"html.parser").findAll("img",{"class":"afg-img"})
a = [i for i in range(0, len(bsObj) )]
shuffle(a)
i = 0

TOKEN_TELEGRAM = os.environ['TOKEN_TELEGRAM']

def start(bot,update):
	bot.sendMessage(chat_id = update.message.chat_id, text = "Welcome")

updater = Updater(TOKEN_TELEGRAM) 
dp = updater.dispatcher
updater.dispatcher.add_handler(CommandHandler('start', start))

def sendNews(bot, job):
	global bsObj,a,i
	for b in range(15):
		try:
			index = a[i]
			photo = bsObj[index].attrs['src']
			text = bsObj[index].attrs['title']
			blob = TextBlob(text) 
			caption = text + "\n\n" + str( blob.translate(to="en")  ) 
		except Exception as e:
			print(e)
			return
		if len(caption) > 200:
			caption = caption[0:197] + "..."
		bot.sendPhoto(chat_id = 31923577, photo = photo, caption = caption)
		i = (i + 1) % len(bsObj)

j = updater.job_queue

utc_offset_heroku = time.localtime().tm_gmtoff / 3600
hour = HOUR_I_WANNA_GET_MESSAGE + ( int(utc_offset_heroku) - 2 ) # 2 is my offset
time2 = datetime.time(hour ,MINUTES_I_WANNA_GET_MESSAGE)

j.run_daily(sendNews, time2 )
updater.start_polling()
updater.idle()
