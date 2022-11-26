from bs4 import BeautifulSoup
import requests
import datetime
import urllib3
import fitz
import re
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # type: ignore
WD = os.getcwd()+"/pdfs/"
WD2 = os.getcwd()+"/imgs/"

def escolhe_data(cardapios):
    dia_a = datetime.datetime.now().day

    for c in cardapios:
        dia_c = c.get('href')[-8:-6]
        if int(dia_c) < dia_a:
            return c.get('href') 
        elif (int(dia_c)-2) > dia_a:
            return c.get('href')


def to_img(name, date):
    doc = fitz.open(name)
    page = doc.load_page(1)  
    pix = page.get_pixmap(dpi=300)
    output = f"{WD2}cardapio-{date}.png"
    pix.save(output)
        

def download_cardapios():
    URL = "https://ru.unb.br/index.php/cardapio-refeitorio/"
    page = requests.get(URL, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    cardapios = soup.find_all(href=re.compile("Gama"))
    c = escolhe_data(cardapios)
    date = c[-8:-4]

    c_url = "".join(["https://ru.unb.br", c])
    response = requests.get(c_url, verify=False)
    name = f"{WD}cardapio-{date}.pdf"   

    if not os.path.isfile(name):
        pdf = open(name, 'wb')
        pdf.write(response.content)
        pdf.close()
        to_img(name, date)