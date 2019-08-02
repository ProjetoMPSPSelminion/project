from bs4 import BeautifulSoup
import os
import requests
import json
import boto3
import re

def login(EMAIL, SENHA):
    r = requests.post('https://www.escavador.com/login', data = {"email":EMAIL,"senha":SENHA})
    cookie = r.cookies
    return cookie

def scraper():
    #dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    #table = dynamodb.Table("Pessoas")
    #NOME = ''
    #for record in event['Records']:
    #   print ("test")
    #   NOME=record["body"]
    #   print(str(NOME))
    NOME = 'Nome'
    EMAIL = 'email'
    SENHA = 'senha'
    cookie = login(EMAIL, SENHA)
        
    url = "https://www.escavador.com/busca?qo=p&q="+str(NOME)
    page = requests.get(url, timeout=15, cookies=cookie)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        divlinks = soup.findAll("a", {"class": "link -dark"})
        pessoas = []
        for links in divlinks:
            if len(links.get("href").split("/")) > 3:
                pessoas.append(links.get("href"))
        for pessoa in pessoas:
            page = requests.get(pessoa)
            soup = BeautifulSoup(page.content, "html.parser")
            id = pessoa.split("/")[4]
            nome = soup.find("h1", {"class": "heading name"})
            if nome:
                nome = nome.getText()
                formacao = soup.find("div", {"id": "formacao"})
                if formacao:
                    todosTitulos = formacao.findAll("p", class_=re.compile(".*-item-formacao"))
                    if todosTitulos:
                        titulos = []
                        dataInicio = []
                        dataFim = []
                        dataFormacao = []
                        faculdades = []
                        for titulo in todosTitulos:
                            titulos.append(titulo.getText())
                        todasDataInicio = formacao.findAll("input", class_=re.compile(".*-item-ano-inicio"), type="hidden",)
                        for data in todasDataInicio:
                            dataInicio.append(data.get("value"))
                        todasDataFim = formacao.findAll("input",class_=re.compile(".*-item-ano-fim"), type="hidden",)
                        for data in todasDataFim:
                            dataFim.append(data.get("value"))
                        for pos, dataI in enumerate(dataInicio):
                            dataFormacao.append(dataI + "-" + dataFim[pos])
                        todasFaculdade = formacao.findAll("a", {"class": "link -color"})
                        for faculdade in todasFaculdade:
                            faculdades.append(faculdade.getText())
                        #response = table.put_item(
                        #    Item={
                        #        "escavid": int(id),
                        #        "nome": str(nome),
                        #        "url": str(pessoa),
                        #        "titulos": list(titulos),
                        #        "datasFormacao": list(dataFormacao),
                        #        "faculdades": list(faculdades),
                        #    }
                        #)
                        ContentUrl = {
                            "escavaid": int(id),
                            "nome": str(nome),
                            "url": str(pessoa),
                            "titulos": list(titulos),
                            "datasFormacao": list(dataFormacao),
                            "faculdades": list(faculdades),
                        }
                        mycwd = os.getcwd()
                        os.chdir("..")
                        
                        with open("outputs/"+id + "data.json", "w", encoding="utf-8") as outfile:
                           json.dump(ContentUrl, outfile, ensure_ascii=False, indent=4)
                        os.chdir(mycwd)
    return "PRONTO"
