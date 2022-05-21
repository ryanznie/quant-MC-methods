# Quant-MC-Methods
Stock Price Predictions Using Monte Carlo Methods

### How to use
To run simulations, enter in ticker name and desired arguments into "simulate()", "compare_times()", or "compare_stocks()". 
Stock movements in the simulations are modeled with geometric brownian motion equations. The parameters are extracted from historical data (5 years if mature stock or lifetime if new stock). The model follows efficient market hypothesis, and assumes that stock movements are random walks.

### Notes
API key is from https://site.financialmodelingprep.com. To use your own API key, you can delete/comment out the "Open and Close" codes and set apiKey = 'Your-API-Key'.
Here is a guide to all the different API calls you can make: https://site.financialmodelingprep.com/developer/docs

### Sources
https://www.investopedia.com/articles/07/montecarlo.asp
