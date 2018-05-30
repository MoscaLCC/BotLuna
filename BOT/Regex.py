import re, random, getopt, datetime, json, sys, os 
from datetime import datetime

class Regex():
    
    def __init__(self, bot):
        self.respostas = {"mes":"Agosto","dia":"20","pais":"Portugal","ano":"1900 e carqueija","cidade":"Cidade Berço","anos":"Os eternos 19.","memoria":"Pelos meus calculos 1Tb no total, com =~ 100Gb livres na partição C:/ e =~ 400Gb livres na partição D:/","ram":"parece infinata, mas deve ser 8Gb","vais":"a nenhures","nasceste":"Bash Ubuntu, Windows","vives":"no submundo da informatica e tu ?","moras":"no enderço de memoria xA23378202B325392","disco":"HDD, mas se me deres um SSD até frito :D :D .... ","veiculo":"Camaro amarelo, kakakakaka","aplido":"BOTtle","signo":"Virgem","idade":"Fui Criado este ano, e tu?","numero de telefone":"não tenho telefone","genero":"sou uma maquina não tenho genero, e o teu?","nome":"LUNA","musico": "Madonna","futebolista":"Cristiano Ronaldo","filme":"Pirata das Caraibas", "musica":"Holiday", "clube":"FC Porto", "carro":"Aston Martin", "comida":"Cozido á Portuguesa"}
        self.bot = bot

    def resp(self,frase):
        now = datetime.now()
        regras = [  (r"te chamas",["Diz tu primeiro","Chamo-me LUNA"]),
                    (r"([qQ]ue dia é hoje|[eE]m que dia estamos)",[lambda x : self.bot.getData()]),
                    (r"([qQ]ue horas são|[dD]iz-me as horas)",[lambda x : self.bot.getHora()]),
                    (r"(\w+) (favorito|favorita|preferido|preferida|que gostas mais|que mais gostas)",[ lambda x : "O " + self.respostas.get(x[0],x[0]+"... não sei")]),
                    (r"[Qq]ual (é|e)? (o|a) (teu|tua) (\w+)",[lambda x : self.respostas.get(x[3],x[3]+"... não sei")]),
                    (r"[qQ](uanto|uantos|uanta|uantas|ue) (\w+) tens", [lambda x : self.respostas.get(x[1],x[1]+"... não sei")]),
                    (r"(([dD]izes-me (o|a))|([dD]iz-me (o|a))|[qQ]ue|([dD]a-me (o|a)))?([mM]etereologia|[Tt]empo de (\w+)|[Tt]empo para (\w+)|[tT]empo que está hoje|[Tt]empo)",[lambda x : self.bot.weather()]),
                    (r"([Qq]ual é o significado de|[oO] que quer dizer|[Dd]iz-me o significado de|[Oo] que significa|[dD]icionario) (\w+)",[lambda x : self.bot.dictionaryQuery(x[1])]),
                    (r"[oO]nde é que (\w+)",[lambda x: self.respostas.get(x, x+"... não sei")]),
                    (r"[Oo] que (.+)? (fazer|fazes|fizeste)",["nada, que seca .. e tu ?","agora, estou a falar contigo", "agora, estou a descansar"]),
                    (r"[eE]m que (\w+)",[lambda x : self.respostas.get(x, x+"...não sei")]),
                    (r"([dD]iz-me|[qQ]uero saber|[Pp]odes me dizer|[qQ]uais são|[dD]a-me)? as? [nN]oticias", [lambda x : self.bot.news()]),
                    (r"([dD]iz-me|[Qq]uero saber|[Pp]odes me dizer|[qQ]uais são|[Dd]a-me)?([Ee]menta|[Aa]lmoço|[Jj]antar)", [lambda x : self.bot.canteenMenu()]),
                    (r"(.*)?[lL]etra da musica (.+) (da|do|das|dos|de) (.+)",[lambda x: self.bot.music(x[1],x[3])]),
                    (r"(.*)?[Tt]radução da musica (.+) (da|do|das|dos|de) (.+)",[lambda x: self.bot.trmusic(x[1],x[3])]),               
                ]            
        for (patt,resps) in regras:
            r = re.findall(patt,frase)
            if r :
                res = random.choice(resps)
                if callable(res) :
                    return res(r[0])
                else:       
                    return res
            else:
                resp = ""
                pesquisa = [(r"([dD]iz|[pP]esquisa|[Pp]rocura|[sS]abes|[qQ]uero saber|[Qq]uem (foi|é|e|era)|[oO] que (é|e|foi|era)|[Cc]omo se) (.+)",[lambda x: self.bot.pesquisa(x[3])])]

                for (patt,resps) in pesquisa:
                    r = re.findall(patt,frase)
                    if r :
                        res = random.choice(resps)
                        if callable(res) :
                            resp +=  res(r[0])
                        else:       
                            resp += res
                        return resp       
        return "Não entendi"
    