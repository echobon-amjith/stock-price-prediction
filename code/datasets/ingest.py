import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
from datasets.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

def index_date(df):
    """
    Convert 'date' column to datetime and set it as the index.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with a 'date' column.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with 'date' as the index and datetime dtype.
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace = True)
    return df

class yf_to_sql:
    """
    Download stock data from Yahoo Finance and manage MySQL database operations.
    
    Attributes
    ----------
    engine : sqlalchemy.engine.Engine
        SQLAlchemy engine for MySQL database connection.
    """
    def __init__(self):
        """
        Initialize the yf_to_sql class with database connection.
        """
        self.engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

    def download(self,ticker, start_date="2015-04-01"):
        """
        Download historical stock data from Yahoo Finance.
        
        Parameters
        ----------
        ticker : str
            Stock ticker symbol (e.g., 'IOC.NS' for IOC stock).
        start_date : str, optional
            Start date for downloading historical stock data in 'YYYY-MM-DD' format.
            Default is "2015-04-01".
        
        Returns
        -------
        pd.DataFrame
            DataFrame containing OHLCV data with reset index.
        """
        df= yf.download(ticker, start= start_date)
        df.reset_index(inplace=True)
        df= pd.DataFrame(df)
        return df

    def sql_push(self,df, table_name):
        """
        Push a DataFrame to a MySQL table.
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to insert into the database.
        table_name : str
            Name of the target table in MySQL.
        
        Notes
        -----
        If the table exists, it will be replaced entirely.
        """
        df.to_sql(name= table_name, con= self.engine,if_exists = "replace", index = False)

    def download_and_push(self,tick, table_name):
        """
        Download stock data and push it directly to a MySQL table.
        
        Parameters
        ----------
        tick : str
            Stock ticker symbol.
        table_name : str
            Name of the target table in MySQL.
        """
        downloaded_data =self.download(tick)
        self.sql_push(downloaded_data, table_name)

    def ioc_data(self):
        """
        Fetch cleaned IOC stock data from MySQL database.
        
        Prompts user to execute 'ioc table prep.sql' in MySQL for data cleaning,
        then retrieves the processed data (date, close, log_close columns).
        
        Returns
        -------
        pd.DataFrame
            DataFrame with date as index and columns: close, log_close.
        
        Notes
        -----
        Requires manual execution of 'ioc table prep.sql' to prepare the 'iocl_clean' table.
        """
        input("Run the query in 'ioc table prep.sql' file in MySQL, once done Press Enter to Continue ")
        df= pd.read_sql("SELECT date, close, log_close FROM iocl_clean", self.engine)
        df= index_date(df)
        return df
