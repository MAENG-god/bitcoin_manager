from box.tools.dataset import dataset
import telegram
import datetime
import time
from box.tools import tools

def hammer(df):
    if tools.candle(df) == "hammer":
        return "hammer"
    
def meteor(df):
    if tools.candle(df) == "meteor":
        return "meteor"
    
def size(df):
    if df.iloc[-2]["size"] > 200:
        return "size"
    
    
def send_message(text):
    tele_token = "5210226721:AAG95BNFRPXRME5MU_ytI_JIx7wgiW1XASU"
    chat_id = 5135122806
    bot = telegram.Bot(token = tele_token)
    bot.sendMessage(chat_id = chat_id, text = text)
    
print("start observing")

while True:
    try:
        data = dataset(symbol="BTC/USDT", timeframe="1h", limit=3)
        print(data)
        if hammer(data) == "hammer":
            text = "현재 캔들 hammer"
            send_message(text)
        if meteor(data) == "meteor":
            text = "현재 캔들 meteor"
            send_message(text)
        if size(data) == "size":
            text = "현재 캔들 변동폭 큼"
            send_message(text)
        while True:
            if data.iloc[-2]['volume'] != dataset(symbol="BTC/USDT", timeframe="1h", limit=10).iloc[-2]['volume']:
                break
            time.sleep(30)
    except Exception as e:
        send_message(e)