# rsi 지표
def rsi(df): 
    au = 0
    u = 0
    ad = 0
    d = 0
    # cur = cur_price - df.iloc[-1]['open']
    for i in df.iloc[-1:-15:-1]['body']:
        if i >= 0:
            au += i
            u += 1
        else:
            ad += -i
            d += 1
    au /= u
    ad /= d
    # if cur >= 0:
    #     au += cur / 14
    # else:
    #     ad += cur / 14 * (-1)
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
    ma3 = sum(df.iloc[-1:-4:-1]['close']) / 3
    ma7 = sum(df.iloc[-1:-8:-1]['close']) / 7
    ma25 = sum(df.iloc[-1:-26:-1]['close']) / 25
    # ma_1 = ma7 - ma25
    
    # ma7 = sum(df.iloc[-2:-9:-1]['close']) / 7
    # ma25 = sum(df.iloc[-2:-27:-1]['close']) / 25
    # ma_2 = ma7 - ma25
    
    # ma7 = sum(df.iloc[-3:-10:-1]['close']) / 7
    # ma25 = sum(df.iloc[-3:-28:-1]['close']) / 25
    # ma_3 = ma7 - ma25
    
   
    # if ma_1 - ma_2 > 0 and ma_2 - ma_3 > 0:
    #     return "long"
    # elif ma_1 - ma_2 < 0 and ma_2 - ma_3 < 0:
    #     return "short"
    if ma3 > ma7 and ma7 > ma25:
        return "long"
    elif ma3 < ma7 and ma7 < ma25:
        return "short"
    
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