# rsi 지표
def rsi(df): 
    au = 0
    u = 0
    ad = 0
    d = 0
    # cur = cur_price - df.iloc[-1]['open']
    for i in df.iloc[-1:-15:-1]['size']:
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
    if df.iloc[-1]['high'] - max(df.iloc[-1]['open'], df.iloc[-1]['close']) > df.iloc[-1]['body'] * 1:
        return "meteor" # 유성형
    if min(df.iloc[-1]['open'], df.iloc[-1]['close']) - df.iloc[-1]['low'] > df.iloc[-1]['body'] * 2:
        return "hammer" # 망치형
        
# 거래량 비교
def volume(df):
    volume1 = df.iloc[-1]['volume']
    volume2 = df.iloc[-2]['volume']
    volume3 = df.iloc[-3]['volume']
    if volume1 > volume2 + volume3:
        return "go"
    else:
        return "stop"