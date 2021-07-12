import pandas as pd
from plotnine import *
from mizani.breaks import date_breaks

df_raw = pd.read_csv("./m5_state_sales.csv")
df = (df_raw
        .assign(ds=lambda df: pd.to_datetime(df.date))
        .assign(year=lambda df: df.ds.dt.year)
        )

theme_set(theme_538)
palette = ['#ee1d52','#f2d803','#69c9d0','#000000']
p = (
        ggplot(df, aes(x='ds', y='sales', color = 'state_id')) +
        geom_point(alpha = .9) +
        geom_line(alpha = .9) +
        scale_x_datetime(breaks=date_breaks('1 Year')) +
        theme(axis_text_x=element_text(angle=45)) +
        xlab('')+
        ggtitle('Sales vs Time by State')+
        scale_color_manual(palette)+
        facet_wrap(facets='state_id',ncol=1)
        )
p.save(filename='../plots/forecast_m5_state_ts.jpg', width=14, height=10)

df = (df.assign(ma_8=df.rolling(window=8).Trips.mean())
        .assign(lag_8=df.shift(8).Trips)
        .assign(ewm_8=lambda df: df.lag_8.ewm(0.9).mean())
)
