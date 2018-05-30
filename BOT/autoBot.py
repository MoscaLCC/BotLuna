from __future__ import print_function
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
import re, random, fileinput, getopt, datetime, json, sys, os 
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.discovery import build
import urllib.request as urllib2
import urllib
import subprocess as s
import pprint
from datetime import datetime
import requests
from flask import Flask, request



class autoBot():
    

    # metodo _init_ é chamdo ao criar um novo objecto desta class
    def __init__(self, nome):
        try:
            memoria = open(nome+'.json','r')
        except FileNotFoundError:
            memoria = open(nome+'.json','w')
            memoria.write('["Luís"]')
            memoria.close()
            memoria = open(nome+'.json','r')
        self.nome = nome
        self.conhecidos = json.load(memoria)
        memoria.close()
        self.FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
        self.VERIFY_TOKEN = 'TESTINGTOKEN'
        self.PAGE_ACCESS_TOKEN = 'EAAEZBu5BhT0IBAGPTXyW34wLD7dxZCxxekenKkbu59FIDoMKZBMLIpBFTNadMapOAgq1tnIk5cAiJvGvnDlFg55FrXpP6HRuQpulMOUZAKdn6QHa86a26TqsmLYOValiIcZCo9EnF4P1vGpp1lfx1M84klEx2rzqGADue8c6ZBIUtcYLPfG0h6'
        self.historico = []
        self.bot = ChatBot('LUNA')
        self.regex = ""
    
    def addRegex(self, regex):
        self.regex = regex

    # metodos principais
    def start(self):
        print('Olá, qual é o seu nome?')
        frase = input('>: ')
        nome = self.catchName(frase)
        frase = self.speakName(nome)
        print(frase)    
        
    def training(self):
        print("Vou aquirir conhecimento")
        self.bot.set_trainer(ListTrainer)

        for _file in os.listdir('chats'):
            print(_file)
            lines = open('chats/' + _file,'r').readlines()
            self.bot.train(lines)

    def listen(self):
        frase = input('>: ')
        frase = frase.lower()
        self.historico.append(frase)
        return frase

    def think(self,frase):
        resultado = self.regex.resp(frase)
        if resultado != "Não entendi":
            return resultado
        if 'aprende' in str(frase):
            return self.learn()

        if 'executa' in str(frase):
            return self.run(frase)                     
        try:
            return self.calculate(frase)
        except:
            pass
            return self.bot.get_response(frase)       

    def thinkfb(self,frase):
        resultado = self.regex.resp(frase)
        if resultado != "Não entendi":
            return "{}".format(resultado)                 
        try:
            return "{}".format(self.calculate(frase))
        except:
            pass
            return "{}".format(self.bot.get_response(frase))
    
    def speak(self,frase):
        print(frase)
        self.historico.append(frase) 

    # metodos secundarios ou auxiliares     

    # metodos auxiliar em start
    def catchName(self,nome):
        if 'o meu nome é ' in nome:
            nome = nome[13:]
        if 'eu sou o ' in nome:
            nome = nome[9:]
        if 'eu sou a ' in nome:
            nome = nome[9:]
        nome = nome.title()
        return nome

    def speakName(self,nome):
        if nome in self.conhecidos:
            frase = 'Olá '
        else:
            frase = 'Muito Prazer '
            self.conhecidos.append(nome)
            memoria = open(self.nome+'.json','w')
            json.dump(self.conhecidos,memoria)
            memoria.close()

        return frase+nome   
    

    def learn(self):  
        chave = input('Digite a palvra chave: ')
        resp = input('Digite a resposta: ')
        self.regex.respostas[chave] = resp
        return 'Aprendido'

    def run(self,frase):
        try:
            plataforma = sys.platform
            comando = str(frase).replace('executa ','')    
            if 'win' in plataforma:
                os.startfile(comando)
            if 'linux' in plataforma:
                try:
                    s.Popen(comando)
                except FileNotFoundError:
                    s.Popen(["xdg-open",comando])   
            if 'linux2' in platforma:
                subprocess.call(["xdg-open",comando])
        except:
            pass
            return 'A tentar Executar!!' 

    def calculate(self,frase):
        resp = str(eval(frase))
        return resp

    # metodos auxiliares em resp

    def getData(self):
        now = datetime.now()
        resp = ""
        resp += str(now.day)
        resp += "/"           
        resp += str(now.month)
        resp += "/"
        resp += str(now.year)

        return resp

    def getHora(self):
        now = datetime.now() 
        resp = ""
        resp += str(now.hour)
        resp += ":"
        resp += str(now.minute)

        return resp

    def weather(self):
        data = urllib2.urlopen("http://api.openweathermap.org/data/2.5/weather?q=Braga,PT&lang=pt&units=metric&type=acurrate&APPID=da5dbcbe2ab4a84aee5e7da42cf7666b")
        html = data.read()
        html = html.decode("utf-8")
        weather = json.loads(html)
        main = str(weather['weather'][0]["main"])
        descricao = str(weather['weather'][0]['description'])
        temperatura = str(weather['main']['temp']) + 'º Graus'
        temperatura_min = str(weather['main']['temp_min'])
        temperatura_max = str(weather['main']['temp_max']) 
        humidade = str(weather['main']['humidity']) + '%'

        resp = '##########################\n\n'
        resp += main + ' => ' + descricao + '\n'
        resp += 'Temperatura: '+ temperatura + ' => ['+ temperatura_min+'º,'+temperatura_max+'º]\n'
        resp += 'Humidade => '+ humidade
        resp += '\n\n##########################'

        return resp

    def dictionaryQuery(self,palavra):
        data = urllib2.urlopen("http://dicionario-aberto.net/search-json/"+palavra)
        html = data.read()
        html = html.decode("utf-8")
        dic = json.loads(html)
     
        i=0
        j=0
        resp = ""
        
        if 'superEntry' in dic :
            for a in dic['superEntry']:
                i=0 
                for b in dic['superEntry'][j]['entry']['sense']:
                    resp += "\n=> "
                    resp += dic['superEntry'][j]['entry']['sense'][i]['def']
                    i += 1
                    resp += "\n"
                j += 1  
        else:
            for b in dic['entry']['sense']:
                resp += "\n=> "
                resp += dic['entry']['sense'][i]['def']
                i += 1
                resp += "\n"
                
        resp = resp.replace('<br/>','')

        return resp

    def news(self):

        data = urllib2.urlopen("https://newsapi.org/v2/top-headlines?country=pt&apiKey=626c562e3c144e6da1303da6f84ebf1f")
        html = data.read()
        html = html.decode("utf-8")
        news = json.loads(html)
        resp = ""

        i = 0
        
        
        for a in news['articles']:
            if i<3:
                resp += "\n################\n" 
                resp += news['articles'][i]['title'] + '\n' 
                resp += news['articles'][i]['url'] +'\n'
            i += 1
        print(resp)
        
        return resp    

    def canteenMenu (self):
        resp = ""
        SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))

        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z' 
        resp += 'Os Proximos 10 Dias:\n'
        events_result = service.events().list(calendarId='5ttsisforihpn2o3blhe3s4tlo@group.calendar.google.com', timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        meses=['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']

        if not events:
            resp += 'Não existem Eventos!'
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            a,b = start.split('T')
            ano, mes, dia = a.split('-')
            data = "Dia "+str(dia)+" de "+ meses[int(mes)-1]
            resp += data + '=>' + event['summary'] +'\n'

        return resp

    def music(self,musica,artista):
        data = urllib2.urlopen("https://api.vagalume.com.br/search.php?art="+artista+"&mus="+musica+"&apikey=0c7c3e61ae19d03c25c287686b61892c")
        html = data.read()
        html = html.decode("utf-8")
        musc = json.loads(html)
        

        resp = '##########################\n\n'
        resp += musc['mus'][0]['text']
        resp += '\n\n##########################'
        return resp

    def trmusic(self,musica,artista):
        data = urllib2.urlopen("https://api.vagalume.com.br/search.php?art="+artista+"&mus="+musica+"&apikey=0c7c3e61ae19d03c25c287686b61892c")
        html = data.read()
        html = html.decode("utf-8")
        musc = json.loads(html)
        

        resp = '##########################\n\n'
        resp += musc['mus'][0]['translate'][0]['text']
        resp += '\n\n##########################'
        return resp    

    def pesquisa(self,palavra):
        resp=""

        resp += '\n\n### '
        resp += "Veja o que encontrei na internet"
        
        resp += ' ###\n\n'
        resp += palavra.upper()
        resp += '\n\n'
                    

        api_key = "AIzaSyCG5rnXXaaTfbrMzfwmB-1khzNeIgtYo2g"
        cse_id = "000833984522281484892:irqcmaus5_e"

        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=palavra, cx=cse_id, num=3).execute()
        searchData = res['items']
        resp += "#######################\n"
        for er in searchData:
            title = er['title']
            resp += "\n=>Titulo: " 
            resp += title
            resp += "\n"
            link = er['link']
            if 'pagemap' in er:
                if 'metatags' in er['pagemap']:
                    if 'og:description' in er['pagemap']['metatags'][0]:
                        description = er['pagemap']['metatags'][0]['og:description']
                        resp += "=>Descrição: "
                        resp += description
                        resp +=  "\n"
            resp += "=>Link: "
            resp += link
            resp += "\n\n#######################\n"
            

        return resp 

    def verify_webhook(self,req):
        if req.args.get("hub.verify_token") == self.VERIFY_TOKEN:
            return req.args.get("hub.challenge")
        else:
            return "incorrect"
    
    def is_user_message(self,message):
        return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))
    
    def speakfb(self,recipient_id, text):
        payload = {
            'message': {
                'text': text
            },
            'recipient': {
                'id': recipient_id
            },
            'notification_type': 'regular'
        }
        auth = {
            'access_token': self.PAGE_ACCESS_TOKEN
        }
        response = requests.post(
            self.FB_API_URL,
            params=auth,
            json=payload
        )
        return response.json()
    
    def listenfb(self):
        text = ""
        sender_id = ""
        if request.method == 'GET':
            return self.verify_webhook(request)

        if request.method == 'POST':
            payload = request.json
            event = payload['entry'][0]['messaging']
            for x in event:
                if self.is_user_message(x):
                    text = x['message']['text']
                    sender_id = x['sender']['id']
            return (sender_id, text)