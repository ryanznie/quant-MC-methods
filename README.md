# quant-MC-methods
Stock price predictions using Monte Carlo methods


## Set Up
**1. Clone repository**

```
git clone https://github.com/ryanznie/quant-MC-methods.git
cd quant-MC-methods
```

**2. Installation**
```
source install.sh
```
After installation, activate the environment with:
```
conda activate quant-mc
```

## Usage

*This project can be used in 3 ways: Web app, CLI tool, or Notebook.*

### 1. Web App

WORK IN PROGRESS

### 2. Command Line

Within `quant-MC-methods` directory, use:
```
python scripts/mc.py --action [action]
```
The default output directory is `plots`.

To open documentations, show a list of commands, and see default values use: 
```
python scripts/mc.py -h
```

Here are a few examples: \
**1.** To plot time series: 
```
python scripts/mc.py --action plot_ts
```
**2.** To fetch data and print mu and std of returns between 01-20-2020 and 03-01-2021:
```
python scripts/mc.py --action fetch_data --start 2020-01-20 --end 2021-03-01
```
**3.** To run 6000 simulations 500 days into the future for PYPL, starting on 2023-01-31, use:
```
python scripts/mc.py --action simulate --num_sim 6000 --start 2023-01-31 --ticker PYPL --time 500
```
**4.** To run two Monte Carlo simulations and show the result histograms side by side, use:
```
python scripts/mc.py --action compare_stocks -n 6000 --ticker MA --ticker2 V
```


### 3. Notebooks

To run simulations, enter in ticker name and desired arguments into `simulate()`, `compare_times()`, or `compare_stocks()`. 
Stock movements in the simulations are modeled with geometric Brownian motion equations. The parameters are extracted from historical data (Version I: 5 years if mature stock or lifetime if new stock; Version II: Defaults from '2020-01-01' to most recent market). The model follows efficient market hypothesis, and assumes that stock movements are random walks.


## Updates:

### IV. 08/17/2023
Version I of CLI tool. Supports basic functions like: `fetch_data()`, `plot_ts()`, `simulate()`, and `compare_stocks()`.

### III. 11/29/2022
Version III added. It uses object oriented programming to allow more flexibility and code interpretation.

### II. 06/18/2022
Version II added. It uses yfinance library from Yahoo Finance instead of Financial Modeling Prep's API. Function docstrings are also updated to improve readability. Historical time frame for data is now flexible for users to choose.

### I. 06/17/2022
Financial Modeling Prep seems to not offer historical daily data for free anymore. I am working on a new version.

## References
* https://www.investopedia.com/articles/07/montecarlo.asp </br>
* https://pypi.org/project/yfinance/
