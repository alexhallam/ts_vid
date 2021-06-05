import numpy as np
import pandas as pd
from plotnine import *
from mizani.breaks import date_breaks
from mizani.formatters import date_format

# read csv
df = pd.read_csv("./data/tourism.csv")

# start with just one time series
df = (df.query("Region == 'Adelaide'")
        .query("State == 'South Australia'")
        .query("Purpose == 'Business'")
        .assign(ds = lambda df: df.Quarter.str.replace(r'(\d+) (Q\d)',r'\1-\2'))
        .assign(ds = lambda df: pd.to_datetime(df.ds))
        .assign(year = lambda df: df.ds.dt.year)
        )

df.info()
df.ds.min()
df.ds.max()
df.Trips.min()
df.Trips.max()
df.ds.max() - df.ds.min()

# quick plot of time series
theme_set(theme_538)
p = (
        ggplot(df, aes(x='ds', y = 'Trips')) +
        geom_point() +
        geom_line() +
        scale_y_continuous(breaks=range(0,260,20)) +
        scale_x_datetime(breaks=date_breaks('1 Years')) +
        theme(axis_text_x=element_text(angle=90)) +
        xlab("")+
        ggtitle("Trips vs Time")
)
p.save(filename = "plots/p.jpg", width = 12, height = 2)

# grouped metrics
df.groupby(['year']).Trips.mean()
df.groupby(['year']).Trips.std()
df.groupby(['year']).Trips.median()

# make new moving averages columns
df = (df.assign(ma_8 = df.rolling(window=8).Trips.mean())
        .assign(lag_8 = df.shift(8).Trips)
        .assign(ewm_09 = df.lag_8.ewm(0.9).mean())
        )
# plot with moving average
palette = ['#ee1d52','#f2d803', '#69c9d0']
p = (
        ggplot(df, aes(x='ds')) +
        geom_point(aes(y = 'Trips')) +
        geom_line(aes(y = 'Trips')) +
        geom_point(aes(y = 'ma_8'), color = palette[0]) +
        geom_line(aes(y = 'ma_8'), color = palette[0]) +
        geom_point(aes(y = 'ewm_09'), color = palette[1]) +
        geom_line(aes(y = 'ewm_09'), color = palette[1]) +
        geom_point(aes(y = 'lag_8'), color = palette[2]) +
        geom_line(aes(y = 'lag_8'), color = palette[2]) +
        scale_y_continuous(breaks=range(0,260,20)) +
        scale_x_datetime(breaks=date_breaks('1 Years')) +
        theme(axis_text_x=element_text(angle=90)) +
        xlab("")+
        ggtitle("Trips vs Time")
)
p.save(filename = "plots/p.jpg", width = 12, height = 2)

# many time series
lags = np.arange(start = 8, stop=17, step=8)
ma = np.arange(start = 8, stop=17, step=8)

df_f = df.assign(**{'lag_{}'.format(i):
    df.groupby(by = ['Purpose'], as_index=False).Trips.transform(lambda c: c.shift(i)) for i in lags})
df_f = df.assign(**{'ma_{}_on_lag8'.format(i):
    df.groupby(by = ['Purpose'], as_index=False).Trips.transform(lambda c: c.rolling(i).mean()) for i in lags})

# part 2 - forecasting with statsmodels

from statsmodels.tsa.holtwinters import ExponentialSmoothing

from statsmodels.tsa.arima_model import ARIMA, ARIMAResults

from statsmodels.tsa.kalmanf import kalmanfilter

from pmdarima import auto_arima

df_ts = df.loc[:,('ds','Trips')]

fit = auto_arima(df_ts.Trips)






