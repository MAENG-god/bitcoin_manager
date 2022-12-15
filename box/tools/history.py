import numpy as np

def history_analysis(df, candle, curRsi):
    upTail = candle['high'] - max(candle['open'], candle['close'])
    downTail = min(candle['open'], candle['close']) - candle['low']
    body = candle['body']
    vol = candle['volume']
    upPerBody = upTail / abs(body)
    downPerBody = downTail / abs(body)
    candleList = []
    for i in range(15, len(df) - 1):
        pastRsi = rsi(df.iloc[i - 14:i + 1])
        pastUpTail = df.iloc[i]['high'] - max(df.iloc[i]['open'], df.iloc[i]['close'])
        pastDownTail = min(df.iloc[i]['open'], df.iloc[i]['close']) - df.iloc[i]['low']
        pastBody = df.iloc[i]['body']
        pastVol = df.iloc[i]['volume']
        
        pastUpPerBody = pastUpTail / (abs(pastBody) + 1)
        pastdownPerBody = pastDownTail / (abs(pastBody) + 1)
        
        result = abs(np.array([upPerBody - pastUpPerBody, downPerBody - pastdownPerBody]))
        result = max(result)
        rsiInd = abs(curRsi - pastRsi)
        volInd = abs(vol - pastVol)
        sameColor = True if body * pastBody > 0 else False
        if result < 0.5 and rsiInd < 2 and sameColor and volInd < 10000:
            if result == 0:
                break
            if df.iloc[i + 1]['body'] > 0:
                candleList.append(1)
            else:
                candleList.append(0)
    if len(candleList) == 0:
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