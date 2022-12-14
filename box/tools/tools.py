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

# 캔들 모양
def candle(df):
    if df.iloc[-2]['high'] - max(df.iloc[-2]['open'], df.iloc[-2]['close']) > abs(df.iloc[-2]['body']) * 1:
        return "meteor" # 유성형
    if min(df.iloc[-2]['open'], df.iloc[-2]['close']) - df.iloc[-2]['low'] > abs(df.iloc[-2]['body']) * 1:
        return "hammer" # 망치형
        
# 거래량 비교
def volume(df):
    volume1 = df.iloc[-1]['volume']
    volume2 = df.iloc[-2]['volume']
    meanVolume = sum(df.iloc[-1:-8:-1]['volume']) / 7
    
    if volume1 > meanVolume:
        return "go"
    else:
        return "stop"
    
#이평선
def ma(df):
    ma5 = sum(df.iloc[-1:-6:-1]['close']) / 5
    ma10 = sum(df.iloc[-1:-11:-1]['close']) / 10
    return ma5 - ma10

#맹's 캔들 5개로 상승추세 하강추세 분석
def five_candle(df):
    candles = df.iloc[-1:-6:-1]['body']
    upCandles = []
    downCandles = []
    for candle in candles:
        if candle > 0:
            upCandles.append(candle)
        else:
            downCandles.append(candle)
    if len(upCandles) == 0 or len(downCandles) == 0:
        return "stop"
    up = sum(upCandles)/len(upCandles)
    down = sum(downCandles)/len(downCandles)
    if up > abs(down):
        return "long"
    else:
        return "short"