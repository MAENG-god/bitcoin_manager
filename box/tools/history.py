import numpy as np

def history_analysis(df, df1, df2, df3, df4, df5, sumVol):
    currentData = np.array([df1, df2, df3, df4, df5])
    candleList = []
    for i in range(14, len(df) - 1):
        pastData = np.array([df.iloc[i - 4]['body'], df.iloc[i - 3]['body'], df.iloc[i - 2]['body'], df.iloc[i - 1]['body'], df.iloc[i]['body']])
        result = abs((currentData - pastData))
        # result = sum(result) / 7
        result = max(result)
        if result < 30:
            if result == 0:
                continue
            pastSumVol = sum(df.iloc[i-6:i+1]['volume'])
            volIndicator = abs(sumVol - pastSumVol)
            if volIndicator < 3000:
                if df.iloc[i + 1]['body'] > 0:
                    candleList.append(1)
                else:
                    candleList.append(0)
    if len(candleList) <= 1:
        return None
    predict = sum(candleList) / len(candleList) * 100
    print("일치 횟수: {}".format(len(candleList)))
    return predict