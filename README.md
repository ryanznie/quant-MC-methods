# quant-MC-methods
Stock Price Predictions Using Monte Carlo Methods


## Set Up
**1. Clone repository**

```
git clone https://github.com/ryanznie/quant-MC-methods.git
cd quant-MC-methods
```

**2. Install and activate environment**

```
conda env create -f environment.yaml
conda activate quant-mc
```

## How to use

### Command Line

Within quant-MC-methods. use:
```
python scripts/mc.py --action [action]
```
The default output directory is `plots`.

Here are a few examples:
1. To plot time series: 
```
python scripts/mc.py --action plot_ts
```
2. To fetch data and print mu and std of returns between 01-20-2020 and 03-01-2021:
```
python scripts/mc.py --action fetch_data --start 2020-01-20 --end 2021-03-01
```
3. To run 6000 simulations 500 days into the future for PYPL, starting on 2023-01-31, use:
```
python scripts/mc.py --action simulate --num_sim 6000 --start 2023-01-31 --ticker PYPL --time 500
```
4. To run two Monte Carlo simulations and show the result histograms side by side, use:
```
python scripts/mc.py --action compare_stocks -n 6000 --ticker MA --ticker2 V
```

To open documentations, show a list of commands, and see default values use: 
```
python scripts/mc.py -h
```

### Notebooks

To run simulations, enter in ticker name and desired arguments into `simulate()`, `compare_times()`, or `compare_stocks()`. 
Stock movements in the simulations are modeled with geometric Brownian motion equations. The parameters are extracted from historical data (Version I: 5 years if mature stock or lifetime if new stock; Version II: Defaults from '2020-01-01' to most recent market). The model follows efficient market hypothesis, and assumes that stock movements are random walks.

## Notebook Version History

### Version III (11/2022)

Changed codes to object oriented.

### Version II (06/2022)

Data is now imported via the yfinance library. To install the library, use *!pip install yfinance* in your notebook or terminal. Please refer to yfinance [documentations](https://pypi.org/project/yfinance/) for any questions or concerns. 

Simulation functions can now also take in arguments for beginning and ending time of historical prices.

### Version I (05/2022)

API key is from [Financial Modeling Prep](https://site.financialmodelingprep.com). To use your own API key, you can delete/comment out the "Open and Close" codes and set apiKey = 'Your-API-Key'. Here is a [guide](https://site.financialmodelingprep.com/developer/docs) to all the different API calls you can make.

## Updates:

### IV. 08/17/2023
Version I of CLI tool completed. Supports basic functions like: `fetch_data()`, `plot_ts()`, `simulate()`, and `compare_stocks()`.

### III. 11/29/2022
Version III added. It uses object oriented programming to allow more flexibility and code interpretation.

### II. 06/18/2022
Version II added. It uses yfinance library from Yahoo Finance instead of Financial Modeling Prep's API. Function docstrings are also updated to improve readability. Historical time frame for data is now flexible for users to choose.

### I. 06/17/2022
Financial Modeling Prep seems to not offer historical daily data for free anymore. I am working on a new version.

## Sources
* https://www.investopedia.com/articles/07/montecarlo.asp </br>
* https://pypi.org/project/yfinance/
