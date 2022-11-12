from tools.dataset import dataset
from tools.tools import *

class Backtest:
    def __init__(self, data, balance, leverage, maxLoseMoney):
        self.data = data        # 4h 차트 데이터
        self.balance = balance  # 잔고
        self.leverage = leverage
        self.fee = 0.0008 * self.leverage        # 매수 매도 총 수수료
        #포지션
        self.position = None
        # 수익률
        self.ror= 1
        # 승리 횟수
        self.win_long = 0
        self.win_short = 0
        # 패배 횟수
        self.lose_long = 0
        self.lose_short = 0
        #체결가
        self.price = 0
        #이익 판매가
        self.win_price = 0
        #손해 판매가
        self.lose_price = 0
        
        self.maxLoseMoney = maxLoseMoney
    
    def excute(self):
        maxLoseMoney = self.maxLoseMoney
        lose = maxLoseMoney / self.leverage
        leverage = self.leverage
        for i in range(26, len(self.data)):
            df = self.data[i - 26:i + 1]
            if self.position == None:
                if rsi(df) > 30 and rsi(df) < 70 and volume(df) == "go":
                    if ma(df) == "short":
                            self.position = "short"
                            self.price = self.data.iloc[i]['close']
                            self.lose_price = self.price * (1 + lose)
                    elif ma(df) == "long":
                            self.position = "long"
                            self.price = self.data.iloc[i]['close']
                            self.lose_price = self.price * (1 - lose)
                elif rsi(df) > 70:
                            self.position = "short"
                            self.price = self.data.iloc[i]['close']
                            self.lose_price = self.price * (1 + lose)
                else:
                            self.position = "long"
                            self.price = self.data.iloc[i]['close']
                            self.lose_price = self.price * (1 - lose)
            elif self.position == "short":
                sell_price = self.data.iloc[i]['close']
                high_price = self.data.iloc[i]['high']
                percent = sell_price / self.price
                if high_price > self.lose_price:
                    self.lose_short += 1
                    self.ror *= 1 - lose * leverage - self.fee
                    self.position = None
                    self.price, sell_price, self.lose_price = 0, 0, 0
                elif sell_price < self.price:
                    self.ror *= 1 + (1 - percent) * leverage - self.fee
                    self.win_short += 1
                    self.position = None
                    self.price, sell_price, self.lose_price = 0, 0, 0
                else:
                    self.ror *= 1 - (percent - 1) * leverage - self.fee
                    self.lose_short += 1
                    self.position = None
                    self.price, sell_price, self.lose_price = 0, 0, 0                    
                    
                    
            else:
                sell_price = self.data.iloc[i]['close']
                low_price = self.data.iloc[i]['low']
                percent = sell_price / self.price
                if low_price < self.lose_price:
                    self.lose_long += 1
                    self.ror *= 1 - lose * leverage - self.fee
                    self.position = None
                    self.price, sell_price, self.lose_price = 0, 0, 0
                elif sell_price > self.price:
                    self.ror *= 1 + (percent - 1) * leverage - self.fee
                    self.win_long += 1
                    self.position = None
                    self.price, sell_price, self.lose_price = 0, 0, 0
                else:
                    self.ror *= 1 + (percent - 1) * leverage - self.fee
                    self.lose_long += 1
                    self.position = None
                    self.price, sell_price, self.lose_price = 0, 0, 0   
    def result(self):
        balance = int(self.ror * self.balance)
        print("수익률: ", self.ror)
        print("롱 승리횟수: ", self.win_long, "롱 패배횟수:", self.lose_long, "롱 승률:", self.win_long/(self.win_long + self.lose_long) * 100)
        print("숏 승리횟수:", self.win_short, "숏 패배횟수: ", self.lose_short, "숏 승률:", self.win_short/(self.win_short + self.lose_short) * 100)
        print("잔고: ", balance, "원")
        return self.ror


data = dataset(symbol="BTC/USDT", timeframe="5m", limit=4*24*1)
backtest = Backtest(data=data, balance=10000, leverage=1, maxLoseMoney=0.1)
backtest.excute()
backtest.result()
