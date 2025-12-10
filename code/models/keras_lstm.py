from tensorflow import keras
import numpy as np
from datetime import date
import pandas as pd
import os

class LSTMmodel:
    """
    LSTM (Long Short-Term Memory) neural network model for time series prediction.
    
    Builds, trains, and uses an LSTM model to predict stock prices based on historical
    closing prices. Supports model training, saving, prediction, and forecasting.
    
    Attributes
    ----------
    model : keras.models.Sequential or None
        The compiled LSTM model.
    x_train : np.ndarray
        Training input sequences with shape (samples, timesteps, features).
    y_train : np.ndarray
        Training target values.
    """
    def __init__(self,x_train, y_train):
        """
        Initialize the LSTMmodel class.
        
        Parameters
        ----------
        x_train : np.ndarray
            Training input sequences with shape (samples, timesteps, features).
        y_train : np.ndarray
            Training target values with shape (samples,).
        """
        self.model= None
        self.x_train = x_train
        self.y_train = y_train

    def build(self):
        """
        Build the LSTM neural network architecture.
        
        Creates a Sequential model with:
        - LSTM layer 1: 128 units, returns sequences
        - LSTM layer 2: 64 units, returns single value
        - Dense layer 1: 25 units
        - Dense layer 2: 1 unit (output)
        """
        self.model = keras.models.Sequential()
        self.model.add(keras.layers.LSTM(128, return_sequences=True, input_shape= (self.x_train.shape[1], 1)))
        self.model.add(keras.layers.LSTM(64, return_sequences=False))
        self.model.add(keras.layers.Dense(25))
        self.model.add(keras.layers.Dense(1))
    
    def compile(self):
        """
        Compile the model with Adam optimizer and Mean Squared Error loss.
        
        Prepares the model for training by specifying the optimization algorithm
        and loss function.
        """
        self.model.compile(optimizer='adam', loss='mean_squared_error')
    
    def train(self,batch_size:int, epochs:int):
        """
        Build, compile, and train the LSTM model.
        
        Parameters
        ----------
        batch_size : int
            Number of samples per gradient update.
        epochs : int
            Number of complete passes through the training dataset.
        """
        self.build()
        self.compile()
        self.model.fit(self.x_train, self.y_train, batch_size, epochs)

    def train_and_save(self, batch_size: int,epochs: int, model_name="lstm_model.h5"):
        self.train(batch_size, epochs)
        full_path = os.path.join("..\code\models", model_name)
        self.model.save(full_path)
        print(f"Model saved to: {full_path}")

    def predict(self, x, MinMax_scaler, model_name):
        full_path = os.path.join("..\code\models", model_name)
        self.model = keras.models.load_model(full_path)
        y_pred = self.model.predict(x)
        y_pred_inv = MinMax_scaler.inverse_transform(y_pred)
        return y_pred_inv
    
    def predict_scaled(self, x, model_name):
        full_path = os.path.join("..\code\models", model_name)
        self.model = keras.models.load_model(full_path)
        y_pred = self.model.predict(x)
        return y_pred
    
    def forecast(self, last_seq, MinMax_scaler, model_name, n_days:int, latest_date: date):
        future_pred = []
        for _ in range(n_days):
            pred_price = self.predict_scaled(last_seq, model_name)
            future_pred.append(pred_price[0,0])
            last_seq = np.append(last_seq[:, 1:, :], [[[pred_price[0, 0]]]], axis=1)
        
        future_pred = np.array(future_pred).reshape(-1,1)
        future_pred = MinMax_scaler.inverse_transform(future_pred)

        future_dates = pd.date_range(latest_date, periods= n_days+1)[1:]
        forecast_df = pd.DataFrame({'Date': future_dates, 'Predicted_Close': future_pred.flatten()})
        forecast_df.set_index('Date', inplace=True)
        return forecast_df