from datetime import datetime, timedelta
from telegram.ext import CallbackContext
from os import path, listdir, getcwd, unlink
from bs4 import BeautifulSoup
from config import Config
import requests
import urllib3
import fitz
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # type: ignore
WD = "".join([getcwd(), "/pdfs/"])
WD2 = "".join([getcwd(), "/imgs/"])


def cache_clean(dir):
    for filename in listdir(dir):
            file_path = path.join(dir, filename)
            try:
                unlink(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


def to_img(name, date):
    doc = fitz.open(name)
    page = doc.load_page(1)  
    pix = page.get_pixmap(dpi=300)
    output = f"{WD2}{date}.png"
    pix.save(output)


def date_picker(menus):
    current_date = datetime.now()
    buffer = False

    for menu in menus:
        if buffer:
            return menu.get('href')
        menu_day = menu.get('href')[-15:-11]
        menu_date = datetime(day=int(menu_day[:2]), month=int(menu_day[2:]), year=current_date.year) + timedelta(days=4) # soma 4 dias na data do cardapio para ver se o dia atual está na mesma semana

        if menu_date >= current_date: 
            return menu.get('href')
        else:
            buffer = True
            

def weekly_send(context: CallbackContext):
    for file in listdir(WD2):
        f = path.join(WD2, file)
        if path.isfile(f):
            pic = open(f, 'rb')
            context.bot.send_photo(chat_id=Config.CHAT_ID, photo=pic)


def weekly_download(context: CallbackContext):
    URL = "https://ru.unb.br/index.php/cardapio-refeitorio/"
    page = requests.get(URL, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    menus = soup.find_all(href=re.compile("Gama"))
    c = date_picker(menus)
    date = c[-15:-11]

    c_url = "".join(["https://ru.unb.br", c])
    response = requests.get(c_url, verify=False)
    name = f"{WD}{date}.pdf" 

    cache_clean(WD)
    cache_clean(WD2)
    
    pdf = open(name, 'wb')
    pdf.write(response.content)
    pdf.close()
    to_img(name, date)
    