import ccxt
import time
from box.tools.dataset import dataset
from box.trade_tool import *

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

state = {
    'position': None,
    'amount': 0,
}

while True:
    data = dataset(symbol="BTC/USDT", timeframe="5m", limit=12 * 24*20)
    try:
        if state['position'] is None:
            enter_position(binance)
        else:
            close_position(binance)
    except Exception as e:
        send_message(e)