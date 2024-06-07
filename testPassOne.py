import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Load data from CSV
data = pd.read_csv('marry_jewelry_data.csv', header=None)
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# Normalize data
X = X / np.max(X)

# Reshape input data for LSTM (samples, timesteps, features)
X = X.reshape(X.shape[0], 1, X.shape[1])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define LSTM model
model = Sequential()
model.add(LSTM(units=128, activation='relu', return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(units=128, activation='relu', return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=1, activation='sigmoid'))

# Define optimizer with a higher learning rate
learning_rate = 0.05
optimizer = Adam(learning_rate=learning_rate)

# Compile model
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

# Fit the model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# Evaluate model on test data
loss, accuracy = model.evaluate(X_test, y_test)
print("Accuracy:", accuracy * 100, "%")
next_value_ran = np.random.randint(0, 10)
# Predict next value
# next_value = int(data.iloc[-1, 1]) + 1  # Increment the second value of the last line
second_last_value = int(data.iloc[-1, 2])
expected_last_value = 3 if second_last_value in [0, 5] else (1 if second_last_value % 2 != 0 else 2)
next_label_range = "green" if expected_last_value == 1 else ("red" if expected_last_value == 2 else "purple")
prediction = f"{next_value_ran},{next_label_range}"

print("Next Value Prediction:", prediction)
