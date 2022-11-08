from tools import tools

def hammer(df):
    if df.iloc[-2]['body'] < 0:
        if tools.candle(df) == "hammer":
            return "hammer"