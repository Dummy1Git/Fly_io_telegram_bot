from bs4 import BeautifulSoup
from googlesearch import search
from dotenv import load_dotenv
import requests
import os
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()

API_KEY = os.getenv('API_KEY')

url='https://masstamilan.dev'

bot=telebot.TeleBot(API_KEY,threaded=True)


def web_crawler(link,message):
    resp = requests.get(link)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title_list=[]
    Audiolink_list=[]
    for row in soup.find('tbody').find_all('tr'):
        col3=row.find_all('td')
        for links in col3:
            link=links.find_all('a')
            for content in link:
                href_value=content.get('href')
                title=content.get('title')
                b=str(content)
                val=b.split()
                if (title is not None and str(title)[:-8:-1]=='spbk023') and ('rel="nofollow"' in val): 
                    Audio_link=url+href_value
                    title_list.append(title)
                    Audiolink_list.append(Audio_link)
    linkd = {title_list[i]: Audiolink_list[i] for i in range(len(title_list))}
    choose(linkd,message)


def choose(dict,message):
    buttons = []
    for key, value in dict.items():
        buttons.append(
        [InlineKeyboardButton(text = key, url = value )]
        )
    keyboard = InlineKeyboardMarkup(buttons)
    bot.reply_to(message,text = f'🎧 <b>{message.text}</b> movie songs 🎧',parse_mode='HTML' ,reply_markup = keyboard)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, text=f'Hi <b>{message.from_user.first_name}</b>👋👋👋 \nWelcome to the channel !! Enter a movie name',parse_mode='HTML')

@bot.message_handler(func= lambda msg: msg.content_type=='text')
def input_query(movie):
    query= movie + ' masstamilan'
    tamilpattu_link='https://tamilpaatu.com/'
    try:
        for j in search(query, tld="co.in", num=1, stop=1, pause=2):
            if j[:23]==tamilpattu_link:
                web_crawler(j,movie)
    except:
        bot.send_message(movie.chat.id,text="Oops!! not found in the website")


if __name__ == "__main__":
    bot.infinity_polling()
