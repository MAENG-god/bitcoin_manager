import ccxt
import time
from box.tools.dataset import dataset
from box.trade_tool import *
from box.predict_tool import PredictNextCandle

api_key = "mF7PJ1yW3YtETZi4uxjDpf5NQGJO2bKedAEMnzBagdux37s5vA8IKnAwhq5CPHZy"
secret = "rsffphg33Pu3CQ1ZUwbiWOYRKKzKGf7hK5YAo9gvjWjYeNYlesTtD170nLE2S84i"

binance = ccxt.binance(config={
    'apiKey': api_key, 
    'secret': secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

#레버리지 설정
markets = binance.load_markets()
symbol = "BTC/USDT"
market = binance.market(symbol)
leverage = 1

resp = binance.fapiPrivate_post_leverage({
    'symbol': market['id'],
    'leverage': leverage
})

balance = binance.fetch_balance()
usdt = balance['free']['USDT']

messeage = "start trading. balance:{}".format(usdt)
send_message(messeage)
print(messeage)

state = {
    'position': None,
    'amount': 0,
    'balance': 0,
    'enterPrice': 0,
    'win': 0,
    'lose': 0,
    'cutPrice': None,
}

while True:
    try:
        ticker = binance.fetch_ticker("BTC/USDT")
        cur_price = ticker['last']
        print(state['position'])
        if state['position'] == None:
            data = dataset(symbol="BTC/USDT", timeframe="1h", limit=12 * 24*20)
            balance = binance.fetch_balance()
            usdt = balance['free']['USDT']
            state['balance'] = usdt
            
            predictor = PredictNextCandle(data)
            predict = predictor.excute()
            enter_position(binance, cur_price, state, predict)
            time.sleep(5)
            
        else:
            if state['position'] == 'long':
                if state['cutPrice'] > cur_price:
                    close_position(binance, cur_price, state)
                    while True:
                        newData = dataset(symbol="BTC/USDT", timeframe="1h", limit=12 * 24*20)
                        if newData.iloc[-2]['body'] - data.iloc[-2]['body'] != 0:
                            break
                        else:
                            time.sleep(10)                    
            elif state['position'] == 'short':
                if state['cutPrice'] < cur_price:
                    close_position(binance, cur_price, state)
                    while True:
                        newData = dataset(symbol="BTC/USDT", timeframe="1h", limit=12 * 24*20)
                        if newData.iloc[-2]['body'] - data.iloc[-2]['body'] != 0:
                            break
                        else:
                            time.sleep(10)    
                            
            newData = dataset(symbol="BTC/USDT", timeframe="1h", limit=12 * 24*20)
            if newData.iloc[-2]['body'] - data.iloc[-2]['body'] != 0:
                close_position(binance, cur_price, state)
                messeage = "승리 횟수:{}, 패배 횟수: {}, 잔고:{}".format(state['win'], state['lose'], state['balance'])
                send_message(messeage)
                messeage = "---------------------\n\n\n------------------------"
                send_message(messeage)
            else:
                time.sleep(1)
            
    except Exception as e:
        send_message(("에러메세지: {}".format(e)))
        print("에러메세지: {}".format(e))