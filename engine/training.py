
# coding: utf-8

# In[5]:

# import necessary modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import cross_val_score


#get_ipython().magic('matplotlib inline')


# In[6]:

production = pd.read_csv("datasets/time_series_60min_singleindex.csv",
                        usecols=(lambda s: s.startswith('utc') | s.startswith('DE')),
                        parse_dates=[0], index_col=0)


production = production.loc[production.index.year == 2016, :]




# save plot
#plt.savefig("figs/solar.png", dpi=200)


# In[11]:

production = production[['DE_wind_generation_actual', 'DE_solar_generation_actual']]


# In[13]:

production = production.dropna() 



# In[17]:

Q1 = production.quantile(0.25)
Q3 = production.quantile(0.75)
IQR = Q3 - Q1


# In[18]:

df = production
df = df[~((df < (Q1-1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))).any(axis=1)]


# In[19]:

weather = pd.read_csv("datasets/weather_data_GER_2016.csv",
                     parse_dates=[0], index_col=0)



weather_by_day = weather.groupby(weather.index).mean()




weather_by_day['T (C)'] = weather_by_day['T'] - 273.15



# merge production_wind_solar and weather_by_day DataFrames
combined = pd.merge(production, weather_by_day, how='left', left_index=True, right_index=True)

weather_by_day = weather_by_day.drop(['h1', 'h2', 'z0', 'lat', 'lon', 'rho', 'p'], axis=1)

weather_by_day.to_csv(r'required_weather.csv')
# drop redundant 'T (C)' column
combined = combined.drop('T (C)', axis=1)

# In[42]:




# In[43]:

X_wind = combined[['v1', 'v2', 'v_50m']]
y_wind = combined['DE_wind_generation_actual']
X_train, X_test, y_train, y_test = train_test_split(X_wind, y_wind, test_size=0.2, random_state=0)

#X_test.to_csv(r'wind_test_X.csv')
#y_test.to_csv(r'wind_test_Y.csv')
# In[49]:

regressor = LinearRegression()  
regressor.fit(X_train, y_train)


filename = 'wind_model.sav'
joblib.dump(regressor, filename)

# In[62]:

scores_wind = cross_val_score(regressor, X_wind, y_wind, cv=5)
print(scores_wind, "\naverage =", np.mean(scores_wind))


# In[47]:

X_solar = combined[['SWGDN', 'T']]
y_solar = combined['DE_solar_generation_actual']
X_train, X_test, y_train, y_test = train_test_split(X_solar, y_solar, test_size=0.2, random_state=0)
#X_test.to_csv(r'solar_test_X.csv')
#y_test.to_csv(r'solar_test_Y.csv')
 
regressor.fit(X_train, y_train)


filename = 'solar_model.sav'
joblib.dump(regressor, filename)

# In[48]:

scores_solar = cross_val_score(regressor, X_solar, y_solar, cv=5)
print(scores_solar, "\naverage =", np.mean(scores_solar))

