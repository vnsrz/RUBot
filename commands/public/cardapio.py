from bs4 import BeautifulSoup
from telegram import Update
import decorators
import requests
import urllib3
import fitz
import re
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # type: ignore
wd = os.getcwd()+"/pdfs/"
wd2 = os.getcwd()+"/imgs/"

def download_cardapios():
    URL = "https://ru.unb.br/index.php/cardapio-refeitorio/"
    page = requests.get(URL, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    cardapios = soup.find_all(href=re.compile("Gama"))

    i = 1

    for c in cardapios:
        c_url = "https://ru.unb.br"+c['href']
        response = requests.get(c_url, verify=False)
        name = f"{wd}cardapio-{i}.pdf"
        pdf = open(name, 'wb')
        pdf.write(response.content)
        pdf.close()
        doc = fitz.open(name)
        page = doc.load_page(1)  
        pix = page.get_pixmap(dpi=300)
        output = f"{wd2}cardapio-{i}.png"
        pix.save(output)
        i+=1

        
@decorators.chat_type.private
def executor(update: Update, ctx):
    download_cardapios()

    chat_id = update.message.chat_id
    for file in os.listdir(wd):
        f = os.path.join(wd, file)
        if os.path.isfile(f):
            doc = open(f, 'rb')
            ctx.bot.send_document(chat_id, doc)
    
    for file in os.listdir(wd2):
        f = os.path.join(wd2, file)
        if os.path.isfile(f):
            pic = open(f, 'rb')
            ctx.bot.send_photo(chat_id, pic)