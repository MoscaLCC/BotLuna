from flask import Flask, request
from autoBot import autoBot
from Regex import Regex

app = Flask(__name__)

bot = autoBot('LUNA')
regex = Regex(bot)
bot.addRegex(regex)

@app.route("/",methods=['GET','POST'])
def start():
    if request.method == 'GET':
        text = bot.listenfb()
        return text
    if request.method == 'POST':
        (sender_id, text) = bot.listenfb()
        bot.speakfb(sender_id, bot.thinkfb(text))
        return "ok"

#FLASK_APP=app.py flask run