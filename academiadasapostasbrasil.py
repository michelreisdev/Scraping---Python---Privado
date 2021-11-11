import requests 
from bs4 import BeautifulSoup

def pageEstatistica():
    header = {'User_Agent':'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36'}
    url = 'https://www.academiadasapostasbrasil.com/stats/match/mundo/eliminatorias-para-a-copa-do-mundo-asia/vietna/japao/RaeQlPGkpQL6o/preview'
    page = requests.get(url, header)
    soup = BeautifulSoup( page.content, 'html.parser')

    times = []

    """ times: [0] => time 01; [1] => 'vs'; [2] => time 02 """
    for a in soup.findAll("div","stats-game-head-teamname")[2]:
        if(len(a.string) > 1):
            times.append(a.text)

    casaProbabilidade = soup.findAll("div","odd")[0]
    casaProbabilidade = float( casaProbabilidade.a.text )

    empateProbabilidade = soup.findAll("div","odd")[1]
    empateProbabilidade = float(empateProbabilidade.a.text)

    foraProbabilidade = soup.findAll("div","odd")[2]
    foraProbabilidade = float( foraProbabilidade.a.text )

    ganhador = times[1]
    if( casaProbabilidade > foraProbabilidade ):
        ganhador = times[2]

    if( empateProbabilidade > foraProbabilidade or empateProbabilidade > casaProbabilidade):
        ganhador = times[0]
    
    return "%s vs %s => %s" % (times[0], times[2], ganhador)

    
print( pageEstatistica() )