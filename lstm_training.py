import pandas as pd 
import numpy as np 

dataset = pd.read_csv("")

# doc_vector = dataset.headline 

#Create slicing windows 
X_train, y_train = [], [] 
look_back = 5 
pred_length = 1 

for i in range(look_back, len(dataset)-pred_length):
    doc_vec = np.array(dataset['headline'][i-look_back:i]) 
    price_vec = np.array(dataset['Close'][i-look_back:i])
    input_vector = np.append(doc_vec, price_vec)
    X_train.append(input_vector)
    y_train.append(dataset['Close'][i])
X_train , y_train = np.array(X_train), np.array(y_train)

input_shape = (X_train.shape[1], X_train.shape[2])

from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import  EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, TensorBoard

regressor = Sequential()

regressor.add(LSTM(units = 32, return_sequences = True, input_shape=input_shape, activation="relu"))
regressor.add(Dropout(0.25))  

regressor.add(LSTM(units = 32, activation="relu"))
regressor.add(Dropout(0.25)) 

regressor.add(Dense(units = 1, activation='relu')) 
regressor.summary()

regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

mcp = ModelCheckpoint('weight/lstm_weight_{epoch:03d}.h5', save_weights_only=True, period=10)
# tb = TensorBoard('logs')
# es = EarlyStopping(monitor='val_loss', min_delta=1e-10, patience=10, verbose=1)
# rlr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, verbose=1)

model_json = regressor.to_json()
with open('lstm_model.json', 'w') as json_file:
    json_file.write(model_json)
print("Saved model")

regressor.fit(X_train, y_train, epochs = 100, shuffle=False,
              callbacks=[mcp], validation_split=0.1, verbose=1, batch_size=16)