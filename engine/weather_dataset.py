
import numpy as np
import pandas as pd

weather = pd.read_csv("datasets/weather_data.csv",
                     parse_dates=[0], index_col=0)


weather = weather.loc[weather.index.year >= 2016, :]
weather_by_day = weather.groupby(weather.index).mean()
print(weather_by_day.columns)
weather_by_day.to_csv(r'required_weather2.csv')
