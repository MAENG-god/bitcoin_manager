import ccxt
import numpy as np
import pandas as pd

def dataset(symbol, timeframe, limit):
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
    symbol = symbol
    btc = binance.fetch_ohlcv(
            symbol=symbol,
            timeframe=timeframe, 
            since=None, 
            limit=limit
        )
    df = pd.DataFrame(data=btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df['body'] = df['close'] - df['open']
    df['size'] = df['high'] - df['low'] 
    df.set_index('datetime', inplace=True)
    
    return df
