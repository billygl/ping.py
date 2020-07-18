import pandas as pd 
import matplotlib.pyplot as plt 
from datetime import datetime
from scipy.interpolate import interp1d
import numpy as np

pd.plotting.register_matplotlib_converters()

def annotate(plt, x, y):
    plt.annotate("%d" % y, xy=(x,y), xytext=(0,7), 
    bbox=dict(boxstyle="round", fc="0.9", ec="gray"),
    textcoords='offset points', ha='center',
    #arrowprops=dict(arrowstyle="->"), ha='right'
    )

df = pd.read_csv("data/data.csv")
df.rename({"Unnamed: 0":"Unnamed"}, axis="columns", inplace=True)
df.drop(['Unnamed'], axis=1, inplace=True)

quantile = .15
y = df['latency']
removed_outliers_y = y.between(y.quantile(quantile), y.quantile(1 - quantile))
index_names = df[~removed_outliers_y].index
df.drop(index_names, inplace=True)

mean = df.mean()
df['avg_latency'] = mean['latency']
df['avg_jitter'] = mean['jitter']

df['datetime'] = df['datetime'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S.%f'))
df['datetime'] = df['datetime'].dt.floor('Min')
ts = df.set_index('datetime')
ts.index = pd.to_datetime(ts.index, unit='s')
ts = ts.resample('300S')
ts = ts.interpolate(method='cubic')

plt.plot(ts.index, ts['latency'],'-',label='latency')
plt.plot(ts.index, ts['jitter'],'-',label='jitter')
plt.plot(ts.index, ts['avg_latency'],'--',label='avg. latency')
plt.plot(ts.index, ts['avg_jitter'],'--',label='avg. jitter')
rows = len(ts)
x = ts.index[rows - 1]
y = ts.iloc[rows - 1].avg_latency
annotate(plt, x, y)
x = ts.index[rows - 1]
y = ts.iloc[rows - 1].avg_jitter
annotate(plt, x, y)
#plt.ylim(0,300)
plt.gcf().autofmt_xdate()
plt.legend()
plt.show()
