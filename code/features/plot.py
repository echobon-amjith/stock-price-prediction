import matplotlib.pyplot as plt

def ts_plot(train, test, forecast_df):
    """
    Plot time series data with training, actual, predicted, and forecasted values.
    
    Visualizes model performance by displaying training data, actual test prices,
    model predictions on test data, and future price forecasts on a single plot.
    
    Parameters
    ----------
    train : pd.DataFrame
        Training data with 'close' column containing historical closing prices.
    test : pd.DataFrame
        Test data with 'close' and 'Predictions' columns containing actual and
        predicted closing prices for the test period.
    forecast_df : pd.DataFrame
        Forecasted closing prices for future dates.
    
    Returns
    -------
    None
        Displays the plot using plt.show().
    
    Notes
    -----
    - Training data is plotted in green
    - Actual test prices are plotted in cyan
    - Predicted test prices are plotted in orange
    - Forecasted prices are plotted in blue
    - Figure size is 16x9 inches for better visualization
    
    Examples
    --------
    >>> ts_plot(train_df, test_df, forecast_df)
    """
    plt.figure(figsize= (16,9))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.title('Model')
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Close Price', fontsize=18)
    plt.plot(train['close'], color= 'green', label= 'training data')
    plt.plot(test['close'], color = 'cyan', label = 'actual stock price')
    plt.plot(test['Predictions'], color = 'orange', label = 'predicted stock price')
    plt.plot(forecast_df,color = 'blue', label = 'Forecast')
    plt.legend()
    plt.show()