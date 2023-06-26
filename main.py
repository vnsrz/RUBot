from os import path, listdir, getcwd, unlink, environ
from datetime import datetime, timedelta
from pdf2image import convert_from_path
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from telegram import Bot
import requests
import urllib3
import re

load_dotenv()

BOT_TOKEN = environ.get("BOT_TOKEN")
ADM_ID = environ.get("ADM_ID")
CHAT_ID = environ.get("CHAT_ID")
WD = "".join([getcwd(), "/pdfs/"])
WD2 = "".join([getcwd(), "/imgs/"])

bot = Bot(token=BOT_TOKEN)
date = datetime.now() + timedelta(days=1)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # type: ignore


def send_img(f, date_start, date_finish, caption):
    if path.isfile(f):
        pic = open(f, "rb")
        bot.send_photo(
            chat_id=CHAT_ID,
            photo=pic,
            caption=f"{caption} - {date_start} a {date_finish}",
        )


def send_menu():
    date_start = date.strftime("%d/%m")
    date_finish = (date + timedelta(days=6)).strftime("%d/%m")

    if darcy:
        bot.send_message(
            chat_id=CHAT_ID,
            text="Não foi encontrado o cardápio atualizado do Gama, então está sendo enviado o do Darcy.",
        )

    f = path.join(WD2, "cafe.jpg")
    send_img(f, date_start, date_finish, "Café")
    print("Café enviado.")

    f = path.join(WD2, "almoco.jpg")
    send_img(f, date_start, date_finish, "Almoço")
    print("Almoço enviado.")

    f = path.join(WD2, "janta.jpg")
    send_img(f, date_start, date_finish, "Jantar")
    print("Jantar enviado.")


def menu_picker(menu_list):
    target = date.strftime("%d-%m")

    for menu in menu_list:
        if target in menu.text:
            return menu.get("href")

    return 0


def cache_clean(dir):
    for filename in listdir(dir):
        file_path = path.join(dir, filename)
        try:
            unlink(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def to_img(file):
    meals = {"cafe": 0, "almoco": 1, "janta": 2}
    images = convert_from_path(file)

    for meal in meals:
        images[meals[meal]].save(f"{WD2}{meal}.jpg", "JPEG")


def download_menu(url):
    response = requests.get(url, verify=False)
    name = f"{WD}{date.strftime('%d-%m')}.pdf"

    cache_clean(WD)
    cache_clean(WD2)

    pdf = open(name, "wb")
    pdf.write(response.content)
    pdf.close()
    to_img(name)
    print("Cardapio baixado.")


def find_menu():
    global darcy
    URL = "https://ru.unb.br/index.php/cardapio-refeitorio/"
    page = requests.get(URL, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")

    menu_list = soup.find_all(href=re.compile("Gama"))
    menu = menu_picker(menu_list)
    darcy = 0

    if not menu:
        menu_list = soup.find_all(href=re.compile("Darcy_Ribeiro"))
        menu = menu_picker(menu_list)
        if not menu:
            bot.send_message(
                chat_id=ADM_ID,
                text="Nenhum cardápio encontrado.\nhttps://ru.unb.br/index.php/cardapio-refeitorio/",
            )
            return 0
        else:
            darcy = 1

    print("Cardapio encontrado.")
    menu_url = "".join(["https://ru.unb.br", menu])
    download_menu(menu_url)
    return 1


if __name__ == "__main__":
    if find_menu():
        send_menu()
