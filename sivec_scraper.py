from bs4 import BeautifulSoup
import os
import requests
import json
import boto3
import re

def login(EMAIL, SENHA, URL, COOKIE):
    r = requests.post(URL, data = {"email":EMAIL,"senha":SENHA}, cookies = COOKIE)
    cookie = r.cookies
    return cookie

def scraper():
    #dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    #table = dynamodb.Table("Pessoas")
    #NOME = ''
    
    EMAIL = 'fiap'
    SENHA = 'mpsp'
    URL = 'http://ec2-18-231-116-58.sa-east-1.compute.amazonaws.com/login'
    COOKIE = ''
    cookieMapa = login(EMAIL, SENHA, URL, COOKIE)
    print(cookieMapa)
    COOKIE = cookieMapa
    URL = 'http://ec2-18-231-116-58.sa-east-1.compute.amazonaws.com/sivec/login.html'
    cookieSivec = login(EMAIL, SENHA, URL, COOKIE)
    
    page = requests.get("http://ec2-18-231-116-58.sa-east-1.compute.amazonaws.com/sivec/pagina6-resultado.html", timeout= 15, cookies= cookieSivec)
    soup = BeautifulSoup(page.content, "html.parser")
    print(soup.prettify)
    #for record in event['Records']:
    #   print ("test")
    #   NOME=record["body"]
    #   print(str(NOME))
    ##NOME = os.environ['Nome']
    #EMAIL = os.environ['Email']
    #SENHA = os.environ['Senha']
    #cookie = login(EMAIL, SENHA)
    
    
    #url = "https://www.escavador.com/busca?qo=p&q="+str(NOME)
    #page = requests.get(url, timeout=15, cookies=cookie)
    #if page.status_code == 200:
    #    soup = BeautifulSoup(page.content, "html.parser")
    #    divlinks = soup.findAll("a", {"class": "link -dark"})
    #    pessoas = []
    #    for links in divlinks:
    #        if len(links.get("href").split("/")) > 3:
    #            pessoas.append(links.get("href"))
    #    for pessoa in pessoas:
    #        page = requests.get(pessoa)
    #        soup = BeautifulSoup(page.content, "html.parser")
    #        id = pessoa.split("/")[4]
    #        nome = soup.find("h1", {"class": "heading name"})
    #        if nome:
    #            nome = nome.getText()
    #            formacao = soup.find("div", {"id": "formacao"})
    #            if formacao:
    #                todosTitulos = formacao.findAll("p", class_=re.compile(".*-item-formacao"))
    #                if todosTitulos:
    #                    titulos = []
    #                    dataInicio = []
    #                    dataFim = []
    #                    dataFormacao = []
    #                    faculdades = []
    #                    for titulo in todosTitulos:
    #                        titulos.append(titulo.getText())
    #                    todasDataInicio = formacao.findAll("input", class_=re.compile(".*-item-ano-inicio"), type="hidden",)
    #                    for data in todasDataInicio:
    #                        dataInicio.append(data.get("value"))
    #                    todasDataFim = formacao.findAll("input",class_=re.compile(".*-item-ano-fim"), type="hidden",)
    #                    for data in todasDataFim:
    #                        dataFim.append(data.get("value"))
    #                    for pos, dataI in enumerate(dataInicio):
    #                        dataFormacao.append(dataI + "-" + dataFim[pos])
    #                    todasFaculdade = formacao.findAll("a", {"class": "link -color"})
    #                    for faculdade in todasFaculdade:
    #                        faculdades.append(faculdade.getText())
    #                    response = table.put_item(
    #                        Item={
    #                            "escavid": int(id),
    #                            "nome": str(nome),
    #                            "url": str(pessoa),
    #                            "titulos": list(titulos),
    #                            "datasFormacao": list(dataFormacao),
    #                            "faculdades": list(faculdades),
    #                        }
    #                    )
    #                    #ContentUrl = {
    #                    #    "escavaid": int(id),
    #                    #    "nome": str(nome),
    #                    #    "url": str(pessoa),
    #                    #    "titulos": list(titulos),
    #                    #    "datasFormacao": list(dataFormacao),
    #                    #    "faculdades": list(faculdades),
    #                    #}
    #                    #mycwd = os.getcwd()
                        #os.chdir("..")
                        #
                        #with open("outputs/"+id + "data.json", "w", encoding="utf-8") as outfile:
                        #   json.dump(ContentUrl, outfile, ensure_ascii=False, indent=4)
                        #os.chdir(mycwd)

    return "PRONTO"
scraper()