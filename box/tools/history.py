import numpy as np

def history_analysis(df, candle1, candle2, curRsi, curMa):
    prevCandle = abs(candle2['body'] / candle2['size'])
    curCandle = abs(candle1['body'] / candle1['size'])
    curVol = candle1['volume'] / candle2['volume']
    candleList = []
    for i in range(15, len(df) - 1):
        pastRsi = rsi(df.iloc[i - 14:i + 1])
        pastMa = ma(df.iloc[i - 10:i + 1])
        pastPrevCandle = abs(df.iloc[i - 1]['body'] / df.iloc[i - 1]['size'])
        pastCurCandle = abs(df.iloc[i]['body'] / df.iloc[i]['size'])
        pastVol = df.iloc[i]['volume'] / df.iloc[i - 1]['volume']
        
        result = abs(np.array([1 - ((prevCandle + 1) / (pastPrevCandle + 1)), 1 - ((curCandle + 1) / (pastCurCandle + 1))]))
        result = max(result)
        sameColor1 = True if candle2['body'] * df.iloc[i - 1]['body'] > 0 else False
        sameColor2 = True if candle1['body'] * df.iloc[i]['body'] > 0 else False
        
        rsiInd = abs(curRsi - pastRsi)
        volInd = 1 - curVol / pastVol
        if result < 0.1 and sameColor1 and sameColor2 and rsiInd < 5 and volInd < 0.1:
            if result == 0:
                break
            if df.iloc[i + 1]['body'] > 0:
                candleList.append(1)
            elif df.iloc[i + 1]['body'] < 0:
                candleList.append(0)
    if len(candleList) <= 1:
        return None
    predict = sum(candleList) / len(candleList) * 100
    print("일치 횟수: {}".format(len(candleList)))
    return predict

def rsi(df): 
    au = 0
    ad = 0

    for i in df.iloc[-2:-16:-1]['body']:
        if i >= 0:
            au += i
        else:
            ad += -i
    au /= 14
    ad /= 14

    cur =  df.iloc[-1]['body']
    if cur > 0:
        au = (13 * au + cur) / 14
        ad = ad * 13 / 14
    else:
        au = au * 13 / 14
        ad = (13 * ad - cur) / 14
    
    rs = au / ad
    rsi = rs / ( 1 + rs) * 100
    
    return rsi

def ma(df):
    ma5 = sum(df.iloc[-1:-6:-1]['close']) / 5
    ma10 = sum(df.iloc[-1:-11:-1]['close']) / 10
    return ma5 - ma10