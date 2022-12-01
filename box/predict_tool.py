from .tools.dataset import dataset
from .tools.tools import *
from .tools.history import *

class PredictNextCandle():
    def __init__(self, df):
        self.df = df
        
    def predict(self, df, dfRsi):
        percent = history_analysis(self.df, df.iloc[0]['body']/df.iloc[0]['volume'], df.iloc[1]['body']/df.iloc[1]['volume'], df.iloc[2]['body']/df.iloc[2]['volume'], df.iloc[3]['body']/df.iloc[3]['volume'], df.iloc[4]['body']/df.iloc[4]['volume'], dfRsi)
        if percent == None:
            return "none"
        elif percent > 60:
            print("올라갈 확률:{}".format(percent))
            return "up"
        elif percent < 40:
            print("내려갈 확률:{}".format(100 - percent))
            return "down"
        else:
            return "none"
    def excute(self):
        df = self.df[-6:-1]
        dfRsi = rsi(self.df[-16 : -1])
        y_hat = self.predict(df, dfRsi)
        return y_hat
data = dataset(symbol="BTC/USDT", timeframe="5m", limit=12 * 24*20)
predict = PredictNextCandle(data)
