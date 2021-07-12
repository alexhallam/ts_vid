import pandas as pd
from plotnine import *
from mizani.breaks import date_breaks

# read csv
df = pd.read_csv("./data/tourism.csv")

# start with just one time series
df = (df.query("Region == 'Adelaide'")
        .query("State == 'South Australia'")
        .query("Purpose == 'Business'")
        .assign(ds=lambda df: df.Quarter.str.replace(r'(\d+) (Q\d)', r'\1-\2'))
        .assign(ds=lambda df: pd.to_datetime(df.ds))
        .assign(year=lambda df: df.ds.dt.year)
        )

df
df.info()
df.ds.min()
df.ds.max()
df.Trips.max()
df.Trips.min()
df.ds.min() - df.ds.max()

# quick plot of time series
theme_set(theme_538)
p = (
        ggplot(df, aes(x='ds', y='Trips')) +
        geom_point() +
        geom_line() +
        scale_y_continuous(breaks=range(0, 260, 20)) +
        scale_x_datetime(breaks=date_breaks('1 Year')) +
        theme(axis_text_x=element_text(angle=45)) +
        xlab('')+
        ggtitle('Trips vs Time')
        )
p.save(filename='plots/p1.jpg', width=12, height=2)
p

# grouped metrics
df.groupby(['year']).Trips.mean()
df.groupby(['year']).Trips.std()
df.groupby(['year']).Trips.median()

# make new moving average, lag, and ewm columns
df = (df.assign(ma_8=df.rolling(window=8).Trips.mean())
        .assign(lag_8=df.shift(8).Trips)
        .assign(ewm_8=lambda df: df.lag_8.ewm(0.9).mean())
        )
df.to_csv("./data/df_out.csv",index=False)

palette = ['#ee1d52','#f2d803', '#69c9d0']
#palette = ['red','yellow', 'blue']
# plot with new features
p = (
        ggplot(df, aes(x='ds')) +
        geom_point(aes(y='Trips')) +
        geom_line(aes(y='Trips')) +
        geom_point(aes(y='ma_8'), color=palette[0]) +
        geom_line(aes(y='ma_8'), color=palette[0]) +
        geom_point(aes(y='ewm_8'), color=palette[1]) +
        geom_line(aes(y='ewm_8'), color=palette[1]) +
        geom_point(aes(y='lag_8'), color=palette[2]) +
        geom_line(aes(y='lag_8'), color=palette[2]) +
        scale_y_continuous(breaks=range(0, 260, 20)) +
        scale_x_datetime(breaks=date_breaks('1 Year')) +
        theme(axis_text_x=element_text(angle=90)) +
        xlab('')+
        ggtitle('Trips vs Time')
        )
p.save(filename='plots/p2.jpg', width=12, height=2)
p
