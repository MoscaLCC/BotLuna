#!/usr/bin/python3
from autoBot import autoBot
from Regex import Regex

bot = autoBot('LUNA')
regex = Regex(bot)
bot.addRegex(regex)

bot.start()
#bot.training()

while True :
    frase = bot.listen()
    bot.speak(bot.think(frase))

