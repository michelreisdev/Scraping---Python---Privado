import requests 
from bs4 import BeautifulSoup
import configparser
import os

path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
config = configparser.ConfigParser()
config.read(os.path.join(path, 'academiadasapostasbrasil.ini'))
param = config["CONFIG"]
pageList = param["pageList"]
pageInicialInt = param["pageInicialInt"]
pagefinalInt = param["pagefinalInt"]

def pageEstatistica(url):
    header = {'User_Agent':'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36'}
    page = requests.get(url, header)
    soup = BeautifulSoup( page.content, 'html.parser')

    times = []

    """ times: [0] => time 01; [1] => 'vs'; [2] => time 02 """
    for a in soup.findAll("div","stats-game-head-teamname")[2]:
        if(len(a.string) > 1):
            times.append(a.text)


    dataJogo = soup.findAll("li","gamehead")[1]

    if(soup.findAll("div","preview_bet") == []):
        return "%s x %s: Jogo Finalizado" % (times[0], times[2])
    else:
        tips = soup.findAll("div","preview_bet")[0]
        tips = tips.p.text
        return "%s \n%s x %s\n<em>%s</em> \n\n" % (dataJogo.text, times[0], times[2], tips)
  
def previews(url):
    header = {'User_Agent':'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36'}
    page = requests.get(url, header)
    soup = BeautifulSoup( page.content, 'html.parser')
    a = []
    for x in range(9):
        tips = soup.findAll("div","preview_item list")[x]
        tips = tips.findAll("a",href=True)[0]
        a.append( pageEstatistica(tips['href']) )
    return a
print("_______________________________________________________________")

pageInicial = int(pageInicialInt)
pageFinal = int(pagefinalInt)
arq = []

while pageFinal >= pageInicial:
    url = f"https://www.academiadasapostasbrasil.com/previews/page/{pageInicial}"
    arq.append( previews( url ))
    pageInicial = pageInicial + 1
    
arq.append( "\n\nTotal: 35" )
with open(os.path.join(path, 'preview.txt'),"w") as arquivo:
    for jogos in arq:
        for jogos2 in jogos:
            arquivo.write(jogos2)