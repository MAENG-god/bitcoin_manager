import numpy as np

def history_analysis(df, df1, df2, df3, df4, df5):
    currentData = np.array([df1, df2, df3, df4, df5])
    candleList = []
    for i in range(5, len(df)):
        pastData = np.array([df.iloc[i - 4]['body'], df.iloc[i - 3]['body'], df.iloc[i - 2]['body'], df.iloc[i - 1]['body'], df.iloc[i]['body']])
        result = abs((currentData - pastData)) ** 0.5
        result = sum(result) / 5
        if result < 1.5:
            if df.iloc[i + 1]['body'] > 0:
                candleList.append(1)
            else:
                candleList.append(0)
    predict = sum(candleList) / len(candleList) * 100
    print(predict)
    return predict