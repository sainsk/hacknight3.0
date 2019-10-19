import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import sys
import random
import requests

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
import numpy as np
import pickle

name = sys.argv[1]

regressor = None

df = pd.read_csv("http://www.moneycontrol.com/tech_charts/nse/his/"+name+".csv",
                 names=["Date", "Open", "High", "Low", "Close", "Volume", "x", "y", "z", "a"])
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
dataset = df[["Open", "High", "Low", "Close", "Volume"]]
training_set = dataset['Close']
training_set = pd.DataFrame(training_set)
sc = MinMaxScaler(feature_range=(0, 1))
training_set_scaled = sc.fit_transform(training_set)
# Creating a data structure with 60 timesteps and 1 output
X_train = []
y_train = []
for i in range(60, len(dataset)):
    X_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

# Reshaping
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

if regressor == None:
    regressor = Sequential()

    # Adding the first LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units=50, return_sequences=True,
                       input_shape=(X_train.shape[1], 1)))
    regressor.add(Dropout(0.2))

    # Adding a second LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units=50, return_sequences=True))
    regressor.add(Dropout(0.2))

    # Adding a third LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units=50, return_sequences=True))
    regressor.add(Dropout(0.2))

    # Adding a fourth LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units=50))
    regressor.add(Dropout(0.2))

    # Adding the output layer
    regressor.add(Dense(units=1))

    # Compiling the RNN
    regressor.compile(optimizer='adam', loss='mean_squared_error')

    # Fitting the RNN to the Training set
    regressor.fit(X_train, y_train, epochs=2, batch_size=32)

    pickle_out = open(name+".pickle", "wb")
    pickle.dump(regressor, pickle_out)

ans = []
values = []
for i in range(7):
    X_test = np.array([training_set_scaled[-60:]])
    # Reshaping
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predicted_stock_price = regressor.predict(X_test)
    training_set_scaled = np.append(training_set_scaled, predicted_stock_price)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)
    ans.append(predicted_stock_price[0][0])
    low_val = predicted_stock_price[0][0]
    r1 = random.randint(3, 8)
    high_val = low_val + (low_val * r1/100)
    low_val = round(low_val, 2)
    high_val = round(high_val, 2)

    values.append([low_val , high_val])



def smsMethod(cmp, contact):
    sms = "Prediction\nLow - High"
    for x in cmp:
      sms +="\n" + str(x[0]) +" - " + str(x[1])
    sms += "\nHappy Trading"
    API_ENDPOINT = "https://alerts.solutionsinfini.com//api/v4/index.php"
    data = {'method': 'sms',
            'message': sms,
            'sender': 'HACKAT',
            'api_key': 'A91862b9c45ff3872032bb46332b1be86',
            'to': contact}
    r = requests.post(url=API_ENDPOINT, data=data)
    print(r.status_code)

contact = int(sys.argv[2])

smsMethod(values,contact)
