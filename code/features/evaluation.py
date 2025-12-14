import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

class ErrorMetrics:
    """
    Calculate and display error metrics for model predictions.
    
    Computes RMSE, MSE, MAE, and MAPE to evaluate prediction accuracy.
    
    Attributes
    ----------
    actual : np.ndarray
        Actual/true values.
    pred : np.ndarray
        Predicted values.
    """
    def __init__(self,actual_y, pred_y):
        """
        Initialize the ErrorMetrics class.
        
        Parameters
        ----------
        actual_y : np.ndarray or pd.Series
            Actual/true target values.
        pred_y : np.ndarray or pd.Series
            Predicted target values.
        """
        self.actual= actual_y
        self.pred = pred_y

    def rmse(self):
        """
        Calculate and print Root Mean Squared Error (RMSE).
        
        RMSE measures the average magnitude of prediction errors, with larger
        errors weighted more heavily. Useful when large errors are undesirable.
        
        Formula: RMSE = sqrt(mean((actual - pred)^2))
        """
        rmse= np.sqrt(np.mean(((self.actual - self.pred) ** 2)))
        return print('RMSE:',rmse)

    def mse(self):
        """
        Calculate and print Mean Squared Error (MSE).
        
        MSE is the average of squared differences between actual and predicted values.
        Lower values indicate better fit. Sensitive to outliers.
        
        Formula: MSE = mean((actual - pred)^2)
        """
        mse= mean_squared_error(self.actual, self.pred)
        return print('MSE:',mse)
    
    def mae(self):
        """
        Calculate and print Mean Absolute Error (MAE).
        
        MAE is the average absolute difference between actual and predicted values.
        More interpretable than MSE as it's in the same units as the target variable.
        
        Formula: MAE = mean(|actual - pred|)
        """
        mae= mean_absolute_error(self.actual, self.pred)
        return print('MAE:', mae)
    
    def mape(self):
        """
        Calculate and print Mean Absolute Percentage Error (MAPE).
        
        MAPE measures the average percentage difference relative to actual values.
        Useful for comparing predictions across different scales or datasets.
        Expressed as a percentage.
        
        Formula: MAPE = mean(|((actual - pred) / actual)| * 100)
        
        Notes
        -----
        May produce unreliable results when actual values are close to zero.
        """
        mape= np.mean(np.abs((self.actual - self.pred)/self.actual)*100)
        return print('MAPE:', mape)

    def all(self):
        """
        Calculate and print all error metrics (RMSE, MSE, MAE, MAPE).
        
        Convenience method to display a comprehensive evaluation of model performance.
        """
        self.rmse()
        self.mse()
        self.mae()
        self.mape()