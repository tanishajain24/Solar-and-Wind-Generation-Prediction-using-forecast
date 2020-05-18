import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
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


if(plant == 'wind'):
	filename = 'wind_model.sav'
else:
	filename = 'solar_model.sav'


loaded_model = joblib.load(filename)

url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={config.API_KEY}"


data = requests.request("GET", url)
response = data.json()

for weather in response["list"]:
	U10 = weather['wind']['speed']
	U2 = powLaw(U10, 2)
	U50 = powLaw(U10, 50)
	gen = loaded_model.predict([[U2, U10, U50]])
	if gen < 0:
		gen = 0
	print(weather['dt_txt'], ' ', gen)
	sys.stdout.flush()







