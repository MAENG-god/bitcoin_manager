from tools.dataset import dataset
from tools.tools import *
from tools.history import *

class predictNextCandle():
    def __init__(self, df):
        self.df = df
        self.epoch = 0
        self.win = 0
        self.wincandle = 0
        self.losecandle = 0
        
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
    def real(self, df):
        if df.iloc[-1]['body'] > 0:
            return "up" 
        else:
            return "down"
    def excute(self):
        for i in range(1398, 1499):
            df = self.df[i - 4:i + 2]
            y_hat = self.predict(df)
            y = self.real(df)
            if y_hat != "none":
                self.epoch += 1
                if y_hat == y:
                    print("예측성공")
                    print("캔들변화량: {}".format(df.iloc[-1]['body']))
                    self.wincandle += abs(df.iloc[-1]['body'])
                    print("-----------------------")
                    self.win += 1
                else:
                    print("예측실패")
                    print("캔들변화량: {}".format(df.iloc[-1]['body']))
                    self.losecandle += abs(df.iloc[-1]['body'])         
                    print("-----------------------")
                    continue
    def summary(self):
        print("예측 정확도: {}%".format(self.win / self.epoch * 100))
        print("이익: {}, 손해: {}".format(self.wincandle, self.losecandle))
        print("총 실행 횟수: {}회".format(self.epoch))
data = dataset(symbol="BTC/USDT", timeframe="1h", limit=12 * 24*20)
predict = predictNextCandle(data)
predict.excute()
predict.summary()
