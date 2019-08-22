#!/usr/bin/env python
# coding=utf-8
from bs4 import BeautifulSoup
import os, logging, mechanicalsoup, pandas, re, urllib.request

link = "http://readshingekinokyojin.com/"
global episodioSelecionado

def escolheIndice(table):
    indice = int(input('Digite o indíce do episódio que deseja assistir : '))
    episodioSelecionado = "Episodios" + "/" + table.loc[indice][0]
    print ("Esse é o episódio selecionado : {}\n".format(episodioSelecionado))
    confirma = (input('Se esse é o episódio que você deseja baixar, digite "s", caso contrário digite "n" : '))
    if (confirma == 's' or confirma == 'S'):
        if not (os.path.exists(episodioSelecionado)):
            os.mkdir(episodioSelecionado)
        return indice, episodioSelecionado
    else:
        return escolheIndice(table)

def downloadImagem(imagemLink, episodioSelecionado):
    nomeArquivo = (imagemLink.rsplit('.png', 1)[0])
    nomeArquivo = (nomeArquivo.rsplit('/', 1)[1])
    print (imagemLink)
    filename = episodioSelecionado + '/' + nomeArquivo
    if not (os.path.exists(filename)):
        try:
            urllib.request.urlretrieve(imagemLink, filename = filename)
            print ("Imagem {} baixada.".format(nomeArquivo))
        except:
            pass
    else:
        print ("Imagem {} já foi baixada.".format(nomeArquivo))

def scrape(link, episodioSelecionado):
    browser = mechanicalsoup.StatefulBrowser()
    page = browser.open(link)
    page = BeautifulSoup(page.text, 'html5lib')
    imagens = page.find_all('div', attrs={'class':'img_container'})

    print ("{} imagens foram encontradas\nIniciando downloads".format(len(imagens)))
    
    for imagem in imagens:
        imagemLink = (imagem.find('img')['src'])
        downloadImagem(imagemLink, episodioSelecionado)
    print ("Download concluído !")

def main():
    browser = mechanicalsoup.StatefulBrowser()
    open = browser.open(link)
    bs = BeautifulSoup(open.text, 'html5lib')
    capitulos = bs.find('ul', attrs={'class':'maniac_posts'})
    #logging.info(capitulos)
    tabela = capitulos.table
    elemento = tabela.find_all('td')
    elemento = list(reversed(elemento))
    table = pandas.read_html(str(tabela))
    table = table[0].reindex(index = table[0].index[::-1])
    table = table.reset_index(drop = True)

    print ('-------- TABELA COM EPISÓDIOS DISPONÍVEIS ---------')
    print (table)
    indice, episodioSelecionado = escolheIndice(table)
    if not (os.path.exists('Episodios')):
        os.mkdir('Episodios')
    episodioLink = elemento[2*indice + 1].find('a')['href']
    print ('\nLink do episódio selecionado : {}'.format(episodioLink))
    scrape (episodioLink, episodioSelecionado)    

if __name__ == '__main__':
    main ()