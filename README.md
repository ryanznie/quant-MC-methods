# Quant-MC-Methods
Stock Price Predictions Using Monte Carlo Methods

### How to use
To run simulations, enter in ticker name and desired arguments into "simulate()", "compare_times()", or "compare_stocks()". 
Stock movements in the simulations are modeled with geometric brownian motion equations. The parameters are extracted from historical data (5 years if mature stock or lifetime if new stock). The model follows efficient market hypothesis, and assumes that stock movements are random walks.

## Version II (06/2022)

Data is imported via the yfinance library. To install the library, use *!pip install yfinance* in your notebook or terminal. Please refer to https://pypi.org/project/yfinance/ for any questions or concerns.

## Version I (05/2022)

API key is from https://site.financialmodelingprep.com. To use your own API key, you can delete/comment out the "Open and Close" codes and set apiKey = 'Your-API-Key'. Here is a guide to all the different API calls you can make: https://site.financialmodelingprep.com/developer/docs

## UPDATES:

### II. 06/18/2022
Version II added. It uses yfinance library from Yahoo Finance instead of an API key from financialmodelingprep.com. Function docstrings are also updated to improve readability.

### I. 06/17/2022
financialmodelingprep.com seems to not offer historical daily data for free anymore. I am working on a new version.

## SOURCES
https://www.investopedia.com/articles/07/montecarlo.asp <br />
https://pypi.org/project/yfinance/
