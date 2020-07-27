#!/usr/bin/python
from bs4 import BeautifulSoup
import requests
import datetime
import os
import shutil

url = "http://semprerci.com.br/livroterapia"
s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
page = s.get(url )

soup_level1=BeautifulSoup(page.content, 'html.parser')
    
postagens1 = soup_level1.find_all(class_="col-sm-9")
postagens2 = postagens1[1].find_all(class_="article-inner")

arquivo_hoje = datetime.date.today().strftime('%Y_%m_%d') + ".xml"
arquivo_anterior = (datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y_%m_%d') + ".xml"

try:
	arquivo = open(arquivo_hoje, 'r')
	print("Arquivo Encontrado")
	arquivo.close()
except  FileNotFoundError:
	i = 0
	arquivo = open(arquivo_hoje, 'w', encoding="utf-8")
	programa=[]
	for tmp in postagens2:
		i=i+1
		img = tmp.find(class_="latest-post-image")
		titulo = img.get('alt')
		referencia = tmp.find(class_="article-info")
		link = "http://semprerci.com.br/" + referencia.a.get('href') 
		programa.append([titulo,link])
		
	print("Iniciou")
	
	arquivo.write("<?xml version="+chr(34)+"1.0"+chr(34)+" encoding="+chr(34)+"UTF-8"+chr(34)+"?>\n<rss xmlns:atom="+chr(34)+"http://www.w3.org/2005/Atom"+chr(34)+" version="+chr(34)+"2.0"+chr(34)+">\n")
	arquivo.write("\n<channel>\n\t<title>Programa Livroterapia - Conscienciologia</title>\n\t<link>http://semprerci.com.br/livroterapia</link>\n")
	arquivo.write("\t<atom:link href="+chr(34)+"http://www.gouget.com.br/tertulias/teste.xml"+chr(34)+" rel="+chr(34)+"self"+chr(34)+" type="+chr(34)+"application/rss+xml"+chr(34)+"/>\n")
	arquivo.write("\t<pubDate>Wed, 19 Dec 2018 09:43:27 CST</pubDate>\n\t<language>pt-BR</language>\n\t<image>\n\t\t<url>http://www.gouget.com.br/tertulias/rci.jpg</url>\n\t</image>\n")
	
	i=0
	for tmp in programa:
		url = tmp[1]
		print(url)
		s = requests.Session()
		s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
		page = s.get(url)
		
		soup = BeautifulSoup(page.content, 'html.parser')
		postagem = soup.find(class_="entry-summary")
		link = postagem.find("a").get('href')
		if "id=" in link:
			link2 = link.split("=")[1]
		else:
			link2 = link.split("/")[5]
		programa[i].append("https://drive.google.com/uc?authuser=0&amp;export=download&amp;id=" + link2)
		
		data = soup.find(class_="entry-date").get_text()
		x= datetime.datetime.strptime(data, "%d/%m/%Y")
		programa[i].append(x.strftime("%a")+', '+ x.strftime("%d") +' '+x.strftime("%B")+' '+x.strftime("%Y")+" 00:00:00 -0300")
		
		tmp2 = programa[i]
		arquivo.write("<item>\n\t<title>"+tmp2[0]+"</title>\n")
		arquivo.write("\t<description><![CDATA[ <b>Programa:</b>"+tmp2[0]+" ]]></description>\n")
		arquivo.write("\t<pubDate>"+tmp2[3]+"</pubDate>\n")
		arquivo.write("\t<enclosure url="+chr(34)+tmp2[2]+chr(34)+"/>\n</item>\n\n")
		
		i=i+1
	print("Pronto")
	arquivo.write("</channel></rss>")
	arquivo.close()

try:
	os.remove(arquivo_anterior)
except:
	pass

try:
	os.remove("livro_terapia.xml")
except:
	pass

try:
	shutil.copy(arquivo_hoje, "livro_terapia.xml")
except:
	pass