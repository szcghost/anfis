import pandas as pd
import talib
import numpy as np
import os

path = os.getcwd()+'\\'

# 读取数据
Data = pd.read_table(path+'res\\999999.txt', delim_whitespace=True, encoding='gbk')
Data = Data[:-1]
Data.columns = ['time', 'openp', 'highp', 'lowp', 'closep', 'volume', 'amount']


# 计算指标，汇总到indicators里
def myMACD(price, fastperiod=12, slowperiod=26, signalperiod=9):
    ewma12 = pd.ewma(price, span=fastperiod)
    ewma26 = pd.ewma(price, span=slowperiod)
    dif = ewma12 - ewma26
    dea = pd.ewma(dif, span=signalperiod)
    bar = (dif - dea)  # 有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
    return dif, dea, bar

#添加数据标签
def getLabel(x):
    if x == 0:
        return 0
    else:
        return int(x/abs(x))

label = list(map(getLabel,np.diff(Data['closep'])))
label = [0]+label

MACD, signal, hist = talib.MACD(Data['closep'].values, fastperiod=12, slowperiod=26, signalperiod=9)
DIF, DEA, BAR = myMACD(Data['closep'].values, fastperiod=12, slowperiod=26, signalperiod=9)
EMA5 = talib.EMA(Data['closep'].values, timeperiod=5)
K, D = talib.STOCH(Data['highp'].values, Data['lowp'].values,
                   Data['closep'].values, fastk_period=14, slowk_period=3,
                   slowk_matype=0, slowd_period=3, slowd_matype=0)
RSI = talib.RSI(Data['closep'].values, timeperiod=14)
indicators = np.column_stack((MACD, DIF, DEA, EMA5, K, D, RSI,label))[35:]

np.savetxt(path+'res\\indicators.txt',indicators,delimiter=',',fmt='%.3f')
