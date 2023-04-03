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


def to_img(name):
    meals = {"cafe": 0, "almoco": 1, "janta": 2}
    doc = fitz.open(name)
    for meal in meals:
        page = doc.load_page(meals[meal])
        pix = page.get_pixmap(dpi=300)
        output = f"{WD2}{meal}.png"
        pix.save(output)


def date_picker(menus):
    global menu_start_date
    global menu_finish_date
    current_date = datetime.now()

    for menu in menus:
        menu_day = menu.get('href')[-17:-12]
        menu_date = datetime(day=int(menu_day[:2]), month=int(menu_day[3:]), year=current_date.year)

        if (menu_date + timedelta(days=4)) >= current_date:  # soma 4 dias na data do cardapio para ver se o dia atual está na mesma semana
            menu_start_date = menu_date
            menu_finish_date = menu_date + timedelta(days=6)
            return menu.get('href')
    
    return 0


def send_menu(context: CallbackContext):
    date_start = menu_start_date.strftime("%d/%m")
    date_finish = menu_finish_date.strftime("%d/%m")

    if darcy:
        context.bot.send_message(chat_id=Config.CHAT_ID, text="Não foi encontrado o cardápio atualizado do Gama, então está sendo enviado o do Darcy.")

    f = path.join(WD2, 'cafe.png')
    if path.isfile(f):
        pic = open(f, 'rb')
        context.bot.send_photo(chat_id=Config.CHAT_ID, photo=pic, caption=f"<b>Café</b> - {date_start} a {date_finish}")

    f = path.join(WD2, 'almoco.png')
    if path.isfile(f):
        pic = open(f, 'rb')
        context.bot.send_photo(chat_id=Config.CHAT_ID, photo=pic, caption=f"<b>Almoço</b> - {date_start} a {date_finish}")

    f = path.join(WD2, 'janta.png')
    if path.isfile(f):
        pic = open(f, 'rb')
        context.bot.send_photo(chat_id=Config.CHAT_ID, photo=pic, caption=f"<b>Jantar</b> - {date_start} a {date_finish}")


def download_menu(context: CallbackContext):
    global darcy
    darcy = 0
    URL = "https://ru.unb.br/index.php/cardapio-refeitorio/"
    page = requests.get(URL, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    menus = soup.find_all(href=re.compile("Gama"))
    c = date_picker(menus)
    
    if not c:
        menus = soup.find_all(href=re.compile("Darcy Ribeiro"))
        c = date_picker(menus)
        if not c:
            context.bot.send_message(chat_id=Config.ADM_ID, text="Nenhum cardápio encontrado.\nhttps://ru.unb.br/index.php/cardapio-refeitorio/")
            return 0
        else:
            darcy = 1

    date = c[-17:-12]
    c_url = "".join(["https://ru.unb.br", c])
    response = requests.get(c_url, verify=False)
    name = f"{WD}{date}.pdf" 

    cache_clean(WD)
    cache_clean(WD2)
    
    pdf = open(name, 'wb')
    pdf.write(response.content)
    pdf.close()
    to_img(name)

    return 1


def weekly_run(context: CallbackContext):
    if download_menu(context):
        send_menu(context)
    