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

    
@bot.message_handler(commands=['trade'])
def trade(message):
    ticker = message.text.split("/trade ")[1].upper()
    try:
        download(ticker)
        confidence_interval,expected_value = interval(f"data/{ticker}.out")
        bot.send_message(message.chat.id,f"Expected price: {round(expected_value,5)}\n1% confidence interval: [{round(confidence_interval[1],5)}, {round(confidence_interval[2],5)}]\n0.1% confidence interval: [{round(confidence_interval[0],5)}, {round(confidence_interval[3],5)}]")
        while not os.path.exists(f"data/{ticker}.M1.out"):
            print("not found")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['alert'])
def alert(message):
    ticker = message.text.split("/alert ")[1].upper()
    try:
        download(ticker)
        confidence_interval,expected_value = interval(f"data/{ticker}.out")
        print(confidence_interval)
        path = r"C:\Users\cormy\AppData\Roaming\MetaQuotes\Terminal\3212703ED955F10C7534BE8497B221F4\MQL4\Files"
        with open(f"{path}\{ticker}.txt", "w") as f:
            f.write(f"{expected_value,confidence_interval[1]},{confidence_interval[2]},{confidence_interval[0]},{confidence_interval[3]}")
            print("Written")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")


print("Start")
bot.infinity_polling()