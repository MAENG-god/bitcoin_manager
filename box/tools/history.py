import numpy as np

def history_analysis(df, df1, df2, df3, df4, df5, dfRsi):
    currentData = np.array([df1, df2, df3, df4, df5]) * 1000
    candleList = []
    for i in range(14, len(df) - 1):
        pastData = np.array([df.iloc[i - 4]['body']/df.iloc[i - 4]['volume'], df.iloc[i - 3]['body']/df.iloc[i - 3]['volume'], df.iloc[i - 2]['body']/df.iloc[i - 2]['volume'], df.iloc[i - 1]['body']/df.iloc[i - 1]['volume'], df.iloc[i]['body']/df.iloc[i]['volume']])
        pastData = pastData * 1000
        result = abs((currentData - pastData)) ** 2
        result = sum(result) / 5
        if result < 30:
            if result == 0:
                continue
            pastRsi = rsi(df.iloc[i - 14:i + 1])
            rsiIndication = (pastRsi - dfRsi) ** 2
            if rsiIndication <= 30:
                if df.iloc[i + 1]['body'] > 0:
                    candleList.append(1)
                else:
                    candleList.append(0)
    if len(candleList) <= 1:
        return None
    predict = sum(candleList) / len(candleList) * 100
    print("일치 횟수: {}".format(len(candleList)))
    return predict

# rsi 지표
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