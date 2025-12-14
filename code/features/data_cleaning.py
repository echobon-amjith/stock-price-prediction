import numpy as np
from sklearn.preprocessing import MinMaxScaler

class PreProcess:
    """
    Preprocessing class for stock price data preparation and train-test splitting.
    
    Handles data scaling, train-test splitting with lookback windows, and reshaping
    for LSTM model input.
    
    Attributes
    ----------
    df : pd.DataFrame
        Input DataFrame with stock price data.
    scaler : sklearn.preprocessing.MinMaxScaler
        MinMax scaler for normalizing data to [0, 1] range.
    scaled_data : np.ndarray
        Scaled closing prices.
    latest_date : pd.Timestamp
        Last date in the DataFrame.
    train_len : int
        Number of samples in the training set.
    """
    def __init__(self,DataFrame,split_by:float):
        """
        Initialize the PreProcess class.
        
        Parameters
        ----------
        DataFrame : pd.DataFrame
            Input DataFrame with stock price data (must have 'close' column).
        split_by : float
            Train-test split ratio (e.g., 0.85 for 85% train, 15% test).
        """
        self.df = DataFrame
        self.scaler = MinMaxScaler(feature_range= (0,1))
        self.scaled_data = None
        self.latest_date = DataFrame.index[-1]
        self.train_len = int(np.ceil(len(DataFrame)*split_by))

    def close_arr(self):
        """
        Extract closing prices as a numpy array.
        
        Returns
        -------
        np.ndarray
            Array of closing prices with shape (n_samples, 1).
        """
        return self.df.filter(['close']).values                     

    def scale_MinMax(self):
        """
        Scale closing prices using MinMax normalization to [0, 1] range.
        
        Fits the scaler on closing prices and stores scaled data in self.scaled_data.
        
        Returns
        -------
        np.ndarray
            Scaled closing prices with shape (n_samples, 1).
        """
        self.scaled_data= self.scaler.fit_transform(self.close_arr())
        return self.scaled_data
    
    def reshape(self,array):
        """
        Reshape array for LSTM input (samples, timesteps, features).
        
        Parameters
        ----------
        array : np.ndarray
            Input array with shape (samples, timesteps).
        
        Returns
        -------
        np.ndarray
            Reshaped array with shape (samples, timesteps, 1).
        """
        return np.reshape(array, (array.shape[0], array.shape[1], 1))
    

    def tt_split(self,lookback_window,reshape=False):
        """
        Split data into train and test sets with lookback window sequences.
        
        Creates sequences for time series prediction where each sequence contains
        'lookback_window' timesteps and predicts the next value.
        
        Parameters
        ----------
        lookback_window : int
            Number of previous timesteps to use as input variables (default: 0).
        reshape : bool, optional
            If True, reshape data to (samples, timesteps, features) for LSTM (default: False).
        
        Returns
        -------
        tuple
            (x_train, y_train, x_test, y_test, last_sequence)
            - x_train : np.ndarray
                Training input sequences.
            - y_train : np.ndarray
                Training target values (unscaled).
            - x_test : np.ndarray
                Test input sequences.
            - y_test : np.ndarray
                Test target values (unscaled closing prices).
            - last_sequence : np.ndarray
                Last 'lookback_window' scaled values for future prediction.
        """
        self.scale_MinMax()
        train_data= self.scaled_data[0:int(self.train_len), :]
        test_data= self.scaled_data[self.train_len - lookback_window: , :]
        last_sequence = self.scaled_data[-lookback_window:, : ]

        x_train = []
        y_train = []
        x_test = []
        y_test = []

        for i in range(lookback_window, self.train_len):
            x_train.append(train_data[i-lookback_window:i, 0])
            y_train.append(train_data[i, 0])

        for i in range(lookback_window, len(test_data)):
            x_test.append(test_data[i-lookback_window: i, 0])
        
        x_train = np.array(x_train)
        y_train = np.array(y_train)
        x_test = np.array(x_test)
        y_test = self.close_arr()[self.train_len:, :]

        if reshape == True:
            x_train = self.reshape(x_train)
            x_test = self.reshape(x_test)
            last_sequence = np.reshape(last_sequence, (1, lookback_window, 1))
        
        return x_train, y_train, x_test, y_test, last_sequence
    
    def train_test(self, pred_y):
        """
        Split DataFrame into train and test sets with predictions appended.
        
        Parameters
        ----------
        pred_y : np.ndarray or pd.Series
            Predicted values for the test set.
        
        Returns
        -------
        tuple
            (train, test)
            - train : pd.DataFrame
                Original training data.
            - test : pd.DataFrame
                Test data with 'Predictions' column added.
        """
        train= self.df[:self.train_len].copy()
        test = self.df[self.train_len:].copy()
        test.loc[:, 'Predictions'] = pred_y

        return train, test
    
        

    
