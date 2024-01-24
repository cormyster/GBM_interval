import telebot
from download_yesterday import download
from find_interval import interval

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
    instrument = message.text.split("/interval ")[1].upper()
    #delete all files in data
    import os
    files = os.listdir("data")
    for file in files:
        print("delete" + file)
        os.remove("data/"+file)
    try:
        download(instrument)
        while not os.path.exists(f"data/{instrument}.M1.out"):
            print("not found")
        confidence_interval,expected_value = interval(f"data/{instrument}.M1.out")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

    bot.send_message(message.chat.id,f"Expected price: {round(expected_value,5)}\n1% confidence interval: [{round(confidence_interval[1],5)}, {round(confidence_interval[2],5)}]\n0.1% confidence interval: [{round(confidence_interval[0],5)}, {round(confidence_interval[3],5)}]")


bot.infinity_polling()