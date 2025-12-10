from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
import pmdarima as pm
import matplotlib.pyplot as plt
import pandas as pd


class EDA:
    """
    Exploratory data analysis helper for time series stock data.

    This class expects a pandas DataFrame with at least a 'close' column
    containing the time series values (closing prices). Methods provide
    decomposition, autocorrelation/partial-autocorrelation plotting,
    stationarity testing and estimation of differencing required for ARIMA.

    Parameters
    ----------
    DataFrame : pandas.DataFrame
        DataFrame containing the time series. Must include a 'close' column
        with numeric values and an index appropriate for time series plotting
        (e.g., DatetimeIndex).

    Notes
    -----
    Methods that display plots call `matplotlib.pyplot.show()` and therefore
    render figures.
    """
    def __init__(self, DataFrame):
        """
        Initialize the EDA helper with a DataFrame.

        Parameters
        ----------
        DataFrame : pandas.DataFrame
            DataFrame containing the time series. Expected to contain a
            'close' column with numeric values.
        """
        self.df = DataFrame

    def decomposition(self, model, period):
        """
        Plot seasonal decomposition of the `close` series.

        Parameters
        ----------
        model : {'additive', 'multiplicative'}
            Type of seasonal decomposition to perform. This value is passed
            directly to `statsmodels.tsa.seasonal.seasonal_decompose`.
        period : int
            Number of observations that make up one seasonal period (for example,
            `365` for daily data with yearly seasonality). Must be a positive integer.

        Returns
        -------
        None
            Displays the decomposition plot using `matplotlib.pyplot.show()`.

        Notes
        -----
        - Uses `extrapolate_trend='freq'` so the trend component is extrapolated
        to the full series length.
        - The decomposition produces `observed`, `trend`, `seasonal` and `resid`
        components and plots them.
        - For small sample sizes or inappropriate `period` values the decomposition
        results may be unreliable.

        Examples
        --------
        >>> eda = EDA(df)
        >>> eda.decomposition('multiplicative', 365)
        """
        decom = seasonal_decompose(self.df['close'], model, period, extrapolate_trend= 'freq')
        decom.plot()
        return plt.show()

    def acf(self, lags):
        """
        Plot the autocorrelation function (ACF) for the 'close' series.

        Parameters
        ----------
        lags : int
            Number of lags to include in the ACF plot.

        Returns
        -------
        None
            Displays the ACF plot and returns `None`.

        Notes
        -----
        The figure is sized to 9x5 inches and layout is tightened.
        """
        fig = plot_acf(self.df['close'], lags = lags)
        fig.set_size_inches((9,5))
        fig.tight_layout()
        return plt.show()
    
    def pacf(self, lags):
        """
        Plot the partial autocorrelation function (PACF) for the 'close' series.

        Parameters
        ----------
        lags : int
            Number of lags to include in the PACF plot.

        Returns
        -------
        None
            Displays the PACF plot and returns `None`.

        Notes
        -----
        The figure is sized to 9x5 inches and layout is tightened.
        """
        pfig = plot_pacf(self.df['close'], lags=lags)
        pfig.set_size_inches((9,5))
        pfig.tight_layout()
        return plt.show()
    
    def acf_pacf(self, lags):
        """
        Show both ACF and PACF plots sequentially.

        Parameters
        ----------
        lags : int
            Number of lags to use for both ACF and PACF plots.

        Returns
        -------
        None
            Calls `self.acf(lags)` and `self.pacf(lags)`, which display plots.
        """
        self.acf(lags)
        self.pacf(lags)

    def adfuller_test(self):
        """
        Run the Augmented Dickey-Fuller (ADF) test on the 'close' series.

        Performs the ADF test with `autolag='AIC'` and returns the primary
        results as a pandas Series for easy display.

        Returns
        -------
        pandas.Series
            Series with the following entries:
            - 'Test statistic' : float
            - 'p-value' : float
            - 'Lags Used' : int
            - 'Number of Observations Used' : int

        Notes
        -----
        A low p-value (commonly < 0.05) suggests the series is stationary.
        """
        adfuller_result = adfuller(self.df['close'], autolag= 'AIC')
        adfuller_output = pd.Series(adfuller_result[:4], index= ['Test statistic', 'p-value', 'Lags Used', 'Number of Observations Used'])
        return adfuller_output
    
    def deg_of_def(self):
        """
        Estimate the degree of differencing required for stationarity.

        Uses `pmdarima.arima.ndiffs` with the 'adf' test to estimate how many
        differences are required to make the 'close' series stationary. The
        estimated value is printed.

        Returns
        -------
        None
            Prints a message with the estimated differencing order.

        Examples
        --------
        >>> eda.deg_of_def()
        The degree of differencing is 1
        """
        iocl_ndiffs = pm.arima.ndiffs(self.df['close'], test = 'adf')
        return print(f'The degree of differencing is {iocl_ndiffs}')