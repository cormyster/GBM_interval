import telebot
from download import download
from find_interval import interval
import os

with open("BOT_KEY.txt", "r") as f:
    BOT_KEY = f.read()
with open("telegram_chat_id.txt", "r") as f:
    chatID = f.read()

bot = telebot.TeleBot(BOT_KEY)

@bot.message_handler(commands=['ping'])
def pong(message):
    bot.send_message(message.chat.id, "pong")

@bot.message_handler(commands=['interval'])
def get_interval(message):
    params = message.text.split("/interval ")[1].split(" -")
    ticker = params[0].upper()
    period = 1
    timeframe = "D"
    for p in params:
        if p.startswith("tf "):
            timeframe = p.split("tf ")[1]
        elif p.startswith("p "):
            period = int(p.split("p ")[1])

    try:
        download(ticker,period)
        confidence_interval,expected_value = interval(f"data/{ticker}.M1.out",timeframe)
        bot.send_message(message.chat.id,f"Expected price: {round(expected_value,5)}\n1% confidence interval: [{round(confidence_interval[1],5)}, {round(confidence_interval[2],5)}]\n0.1% confidence interval: [{round(confidence_interval[0],5)}, {round(confidence_interval[3],5)}]")
        while not os.path.exists(f"data/{ticker}.M1.out"):
            print("not found")
        
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

    


print("Start")
bot.infinity_polling()