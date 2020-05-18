import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import joblib

filename = 'solar_model.sav'

X_test = pd.read_csv("solar_test_X.csv", parse_dates=[0], index_col=0)
Y_test = pd.read_csv("solar_test_Y.csv", parse_dates=[0], index_col=0)

loaded_model = joblib.load(filename)
result = loaded_model.score(X_test, Y_test)
print(result)