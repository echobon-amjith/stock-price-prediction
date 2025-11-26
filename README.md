# Stock Price Prediction
A data science project for predicting stock prices using machine learning techniques, following the Data Science Lifecycle Process.
## Background
I invested in IOC stock with minimal knowledge in the stock market. I missed the opportunity  to sell the stock at a profitable price. Now I need to know before hand when I can sell of the stock at a reasonable profit.
## Project Overview
This project aims to develop and evaluate predictive models for stock price movement using historical market data.
## Prerequisites
- Python 3.9
- create a conda environment using [environment.yml](environments\environment.yml)
## Directory Structure
```
├── code
│   ├── datasets        # code for creating or getting datasets
│   ├── deployment      # code for deploying models
│   ├── features        # code for creating features
│   └── models          # code for building and training models
├── data                # directory is for consistent data placement. contents are gitignored by default.
│   ├── README.md
│   ├── interim         # storing intermediate results (mostly for debugging)
│   ├── processed       # storing transformed data used for reporting, modeling, etc
│   └── raw             # storing raw data to use as inputs to rest of pipeline
├── docs
│   ├── code            # documenting everything in the code directory (could be sphinx project for example)
│   ├── data            # documenting datasets, data profiles, behaviors, column definitions, etc
│   ├── media           # storing images, videos, etc, needed for docs.
│   ├── references      # for collecting and documenting external resources relevant to the project
│   └── solution_architecture.md    # describe and diagram solution design and architecture
├── environments        # Environment configuration files
├── notebooks           # Exploratory analysis and experimentation
├── setup.py            # if using python, for finding all the packages inside of code.
└── tests               # for testing your code, data, and outputs
    ├── data_validation
    └── unit
```
## Data Pipeline
- Using yfinance library in python, the daily OHLCV data of IOC stock from 2015 is festched into MySQL database as a table 
- In MySQL database the table is cleaned to include the non business days data and a new column log_close is added to include the scaled values of the closing price. Both using SQL query.
-  After the data cleaning the data from the SQL databse is then fetched as a dataframe into python for data analysis and modelling.
- For model evaluation the data undergoes train-test split, where 85% of the data is used as training set.
- The training set is used for training the model and the test data is passed on to the model for evaluating the model. 
## Models
[SARIMA Model](https://github.com/ecobon-amjith/stock-price-prediction/issues/8#issue-3653926631)
[LSTM Model](https://github.com/ecobon-amjith/stock-price-prediction/issues/10#issue-3654758030)
## Key Files
- [setup.py](setup.py) - Package configuration and dependencies
- [data/README.md](data/README.md) - Data documentation
- [docs/solution_architecture.md](docs/solution_architecture.md) - Architecture overview
## Contact
[Add contact information or team details]
