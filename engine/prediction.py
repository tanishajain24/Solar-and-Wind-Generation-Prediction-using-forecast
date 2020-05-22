import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from datetime import datetime
import joblib
import math
import requests
import json
import config
import sys

plant = sys.argv[1]
city = sys.argv[2]
#Formula of log wind profile
def logWindProf_1(Uz):
	#Uz=(U/K)*[ln(Z/Zo)]
	K = 0.4
	#For flat terrain with grass Zo is
	Zo = 0.03

	U10 = (Uz/math.log(10, Zo))*K
	U2 = (U10/K)*(math.log(2, Zo))
	U50 = (U10/K)*(math.log(50, Zo))
	return U2,U50


def logWindProf_2(Uz):
	#u2 = uz * 4 . 87 / ln ( 67 . 8 * z − 5 . 42 ) or approx. 0.75 * given velocity at 10m
	return 0.75*Uz

def powLaw(Ur, Z):
	#u = ur*(z/zr)^alpha
	alpha = 0.143 #for neutral stability conditions
	Zr = 10 #average height in weather forecast
	return Ur*(pow((Z/Zr), alpha))

def mean_hist_values(date_time_obj):
	weather_data = weather_hist.loc[(weather_hist.index.month == date_time_obj.month) 
									& (weather_hist.index.hour == date_time_obj.hour) 
									& (weather_hist.index.day == date_time_obj.day), ['rad_direct', 'rad_diffuse']]

	total_rad = weather_data['rad_direct'] + weather_data['rad_diffuse']
	
	return sum(total_rad)/len(total_rad)
	#for weather in weather_data



weather_hist = pd.read_csv("weather_data.csv",
                     parse_dates=[0], index_col=0)

weather_hist = weather_hist.rename(columns={"DE_radiation_direct_horizontal": "rad_direct", 
						"DE_radiation_diffuse_horizontal": "rad_diffuse"})

url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={config.API_KEY}"

data = requests.request("GET", url)
response = data.json()
today = datetime.now().day;

if(plant == 'wind'):
	filename = 'wind_model.sav'
	loaded_model = joblib.load(filename)
	for weather in response["list"]:
		date_time_obj = datetime.strptime(weather['dt_txt'], "%Y-%m-%d %H:%M:%S")
		if(date_time_obj.day > today):
			U10 = weather['wind']['speed']
			U2 = powLaw(U10, 2)
			U50 = powLaw(U10, 50)
			gen = loaded_model.predict([[U2, U10, U50]])[0]
			if gen < 0:
				gen = 0
			print(gen)
			sys.stdout.flush()
else:
	filename = 'solar_model.sav'
	loaded_model = joblib.load(filename)
	for weather in response["list"]:
		date_time_obj = datetime.strptime(weather['dt_txt'], "%Y-%m-%d %H:%M:%S")
		if(date_time_obj.day > today):
			T = weather['main']['temp']
			mean_rad = mean_hist_values(date_time_obj)
			gen = loaded_model.predict([[mean_rad, T]])[0]
			if gen < 0:
				gen = 0
			print(gen)
			sys.stdout.flush()













