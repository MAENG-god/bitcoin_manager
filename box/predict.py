from tools.dataset import dataset
from tools.tools import *
from tools.history import *

class predictNextCandle():
    def __init__(self, df):
        self.df = df
        self.epoch = 0
        self.win = 0
        self.profit = 0
        self.loss = 0
        self.ror = 1
        self.leverage = 10
        self.fee = 0.0008 * self.leverage
        
    def predict(self, df):
        curRsi = rsi(df.iloc[-16:-1])
        curMa = ma(df.iloc[-16:-1])
        percent = history_analysis(self.df, df.iloc[-2], df.iloc[-3], curRsi, curMa)
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
    def real(self, df):
        if df.iloc[-1]['body'] > 0:
            return "up" 
        else:
            return "down"
    def excute(self):
        for i in range(1400, 1498):
            df = self.df[0:i + 2]
            y_hat = self.predict(df)
            y = self.real(df)
            if y_hat != "none":
                self.epoch += 1
                if y_hat == y:
                    if y_hat == "up":
                        if df.iloc[-1]['low']/df.iloc[-1]['open'] < 0.99:
                            print("예측실패")
                            self.ror *= 0.9 - self.fee
                            continue
                    elif y_hat == "short":
                        if df.iloc[-1]['high']/df.iloc[-1]['open'] > 1.01:
                            print("예측실패")
                            self.ror *= 0.9 - self.fee
                            continue
                    print("예측성공")
                    print("캔들변화량: {}".format(df.iloc[-1]['body']))
                    self.profit += abs(df.iloc[-1]['body'])
                    print("-----------------------")
                    self.win += 1
                    if df.iloc[-1]['body'] > 0:
                        self.ror *= 1 + abs(1 - (df.iloc[-1]['close']/df.iloc[-1]['open'])) * self.leverage - self.fee
                    else:
                        self.ror *= 1 + abs(1 - (df.iloc[-1]['close']/df.iloc[-1]['open'])) * self.leverage - self.fee
                else:
                    if y_hat == "up":
                        if df.iloc[-1]['low']/df.iloc[-1]['open'] < 0.99:
                            print("예측실패")
                            self.ror *= 0.9 - self.fee
                            continue
                    elif y_hat == "short":
                        if df.iloc[-1]['high']/df.iloc[-1]['open'] > 1.01:
                            print("예측실패")
                            self.ror *= 0.9 - self.fee
                            continue
                    print("예측실패")
                    print("캔들변화량: {}".format(df.iloc[-1]['body']))
                    self.loss += abs(df.iloc[-1]['body'])         
                    print("-----------------------")
                    if df.iloc[-1]['body'] > 0:
                        self.ror *= 1 - abs(1 - (df.iloc[-1]['close']/df.iloc[-1]['open'])) * self.leverage - self.fee
                    else:
                        self.ror *= 1 - abs(1 - (df.iloc[-1]['close']/df.iloc[-1]['open'])) * self.leverage - self.fee
    def summary(self):
        print("예측 정확도: {}%".format(self.win / self.epoch * 100))
        print("이익: {}, 손해: {}, 수익률:{}%".format(self.profit, self.loss, self.ror * 100 - 100))
        print("총 실행 횟수: {}회".format(self.epoch))
data = dataset(symbol="BTC/USDT", timeframe="4h", limit=12 * 24*20)
predict = predictNextCandle(data)
predict.excute()
predict.summary()