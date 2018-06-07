from fbchat import log, Client
import random
from fbchat.models import *
import operator
import re
from time import *
import datetime
import sys
import unicodedata
from autoBot import autoBot
from Regex import Regex

bot = autoBot('LUNA')
regex = Regex(bot)
bot.addRegex(regex)
bot.start()
bot.training()

def analisa_mensagem(cliente, message_object, thread_id, thread_type):
	resp = ""
	mensagem = str(message_object.text)
	print(mensagem)
	resp = bot.thinkfb(mensagem)
	print(resp)
	return cliente.send(Message(resp), thread_id=thread_id, thread_type=thread_type)


class EchoBot(Client):

	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		self.markAsDelivered(author_id, thread_id)
		self.markAsRead(author_id)

		log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
		
		if author_id != self.uid:
			analisa_mensagem(self, message_object, thread_id, thread_type)


client = EchoBot("luismarqueslcc@gmail.com", "Botspln2018")
client.listen()