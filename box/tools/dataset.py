import ccxt
import numpy as np
import pandas as pd

def dataset(symbol, timeframe, limit):
    api_key = "UbhY6U61Zp51mxCmZgc8OYdHMg9o62O5yBYnzhPAbbkrJpMBHNBuWbrVDW1WXB8I"
    secret = "tByo1L8nH6wrbC6OVNJg2uQFrzqgxBn4a5LijXBGCb6CasqGCm2TeqbbdItKY3R1"

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