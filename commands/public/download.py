from os import path, listdir, getcwd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import urllib3
import fitz
import re


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # type: ignore
WD = "".join([getcwd(), "/pdfs/"])
WD2 = "".join([getcwd(), "/imgs/"])

def get_cardapio():
    data_a = datetime.now()
    downloaded = [f for f in listdir(WD) if path.isfile(path.join(WD, f))]
    if not downloaded:
        download_cardapios()
        return
    file_name = path.basename(downloaded[0])
    downloaded = path.splitext(file_name)[0]
    downloaded = datetime(day=int(downloaded[:2]), month=int(downloaded[2:]), year=data_a.year)

    if data_a > downloaded:
        download_cardapios()

    else:
        print("Cardapio da semana ja baixado.") 


def escolhe_data(cardapios):
    data_a = datetime.now()
    buffer = False

    for c in cardapios:
        if buffer:
            return c.get('href')
        dia_c = c.get('href')[-15:-11]
        data_c = datetime(day=int(dia_c[:2]), month=int(dia_c[2:]), year=data_a.year) + timedelta(days=4) # soma 4 dias na data do cardapio para ver se o dia atual está na mesma semana

        if data_c >= data_a: 
            return c.get('href')
        else:
            buffer = True


def to_img(name, date):
    doc = fitz.open(name)
    page = doc.load_page(1)  
    pix = page.get_pixmap(dpi=300)
    output = f"{WD2}{date}.png"
    pix.save(output)
        

def download_cardapios():
    URL = "https://ru.unb.br/index.php/cardapio-refeitorio/"
    page = requests.get(URL, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    cardapios = soup.find_all(href=re.compile("Gama"))
    c = escolhe_data(cardapios)
    date = c[-15:-11]

    c_url = "".join(["https://ru.unb.br", c])
    response = requests.get(c_url, verify=False)
    name = f"{WD}{date}.pdf"   

    pdf = open(name, 'wb')
    pdf.write(response.content)
    pdf.close()
    to_img(name, date)