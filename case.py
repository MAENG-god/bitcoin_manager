from tools import tools

def hammer(df):
    if tools.candle(df) == "hammer":
        return "hammer"
    
def meteor(df):
    if tools.candle(df) == "meteor":
        return "meteor"
    
def size(df):
    if df.iloc[-1]["size"] > 200:
        return "size"