from .tools.dataset import dataset
from .tools.tools import *
from .tools.history import *

class PredictNextCandle():
    def __init__(self, df):
        self.df = df
        
    def predict(self, df):
        curRsi = rsi(df.iloc[-15:])
        curMa = ma(df.iloc[-15:])
        percent = history_analysis(self.df, df.iloc[-1], df.iloc[-2], curRsi, curMa)
        if percent == None:
            return "none"
        elif percent > 50 and curRsi < 50:
            print("올라갈 확률:{}".format(percent))
            return "up"
        elif percent < 50 and curRsi > 50:
            print("내려갈 확률:{}".format(100 - percent))
            return "down"
        else:
            return "none"
    def excute(self):
        df = self.df[-20:-1]
        y_hat = self.predict(df)
        return y_hat


