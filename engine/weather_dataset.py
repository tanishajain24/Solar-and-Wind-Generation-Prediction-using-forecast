
import numpy as np
import pandas as pd

weather = pd.read_csv("weather_data.csv",
                     parse_dates=[0], index_col=0)

print(weather.loc[(weather.index.month == 3) & (weather.index.hour == 6) & (weather.index.day = 28, :])
