from .tools.dataset import dataset
from .tools.tools import *
from .tools.history import *

class PredictNextCandle():
    def __init__(self, df):
        self.df = df
        
    def predict(self, df):
        sumVol = sum(df.iloc[0:5]['volume'])
        percent = history_analysis(self.df, df.iloc[0]['body'], df.iloc[1]['body'], df.iloc[2]['body'], df.iloc[3]['body'], df.iloc[4]['body'], sumVol)
        if percent == None:
            return "none"
        elif percent > 50:
            print("올라갈 확률:{}".format(percent))
            return "up"
        elif percent < 50:
            print("내려갈 확률:{}".format(100 - percent))
            return "down"
        else:
            return "none"
    def excute(self):
        df = self.df[-6:-1]
        y_hat = self.predict(df)
        return y_hat


