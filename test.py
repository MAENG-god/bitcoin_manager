from box.tools.dataset import dataset
from box.trade_tool import *
from box.predict_tool import PredictNextCandle

data = dataset(symbol="BTC/USDT", timeframe="4h", limit=12 * 24*20)
print(data)