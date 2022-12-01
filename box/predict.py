from tools.dataset import dataset
from tools.tools import *
from tools.history import *

class predictNextCandle():
    def __init__(self, df):
        self.df = df
        self.epoch = 0
        self.win = 0
        
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
    def real(self, df):
        if df.iloc[-1]['body'] > 0:
            return "up" 
        else:
            return "down"
    def excute(self):
        for i in range(900, 1001):
            df = self.df[i - 4:i + 2]
            dfRsi = rsi(self.df[i -14 : i + 1])
            y_hat = self.predict(df, dfRsi)
            y = self.real(df)
            if y_hat != "none":
                self.epoch += 1
                if y_hat == y:
                    print("예측성공")
                    print("-----------------------")
                    self.win += 1
                else:
                    print("예측실패")
                    print("-----------------------")
                    continue
    def summary(self):
        print("예측 정확도: {}%".format(self.win / self.epoch * 100))
        print("총 실행 횟수: {}회".format(self.epoch))
data = dataset(symbol="BTC/USDT", timeframe="5m", limit=12 * 24*20)
predict = predictNextCandle(data)
predict.excute()
predict.summary()
