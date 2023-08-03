
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime
import os
import argparse
from utils import setup_logger


def monte_carlo(args):
    """
    Main
    CLI tool for stock price predictions using Monte Carlo methods
    """

    # actions
    if args.action == 'fetch_data':
        fetch_data(args.ticker, args.start, args.end)
    elif args.action == 'plot_ts':
        plot_ts(args.ticker, args.start, args.end, args.output_dir)
    elif args.action == 'simulate':
        simulate()
    elif args.action == 'compare_times':
        compare_times()
    elif args.action == 'compare_stocks':
        compare_stocks()




def fetch_data(ticker, time_start, time_end):
    """
    Tests API connection
    Fetches data from yfinance and calculates a return column
    """
    data = yf.Ticker(ticker)
    logger.info(f"FETCHING DATA: {ticker} from {time_start} to {time_end}")
    df = data.history(start=time_start, end=time_end, rounding=True)
    logger.debug(f"FETCHED DATA: {ticker} - df shape: {df.shape}")
    df['return'] = (df['Close'] - df['Open']) / df['Open']
    
    print(df.head())
    if df.shape[0] == 0:
        logger.info(f"FETCH UNSUCCESSFUL - SHAPE: {df.shape}")
    else:
        logger.info(f"FETCHED SUCCESSFULLY - SHAPE: {df.shape}")


def plot_ts(ticker, time_start, time_end, output_dir):
    """
    Plots time series of a ticker in a specific time frame
    Stores plots in output_dir in format {ticker}_S{YYYYMMDD}E{YYYYMMDD}.png
    """
    logger.info(f"PLOTTING TICKER: {ticker} from {time_start} to {time_end}")
    data = yf.Ticker(ticker)
    df = data.history(start=time_start, end=time_end, rounding=True)
    logger.debug(f"FETCHED DATA: {ticker} - df shape: {df.shape}")
    fig = plt.figure()
    plt.plot(df['Close'])
    plt.title(f'Time series of {ticker} from {time_start} to {time_end}')
    plt.xlabel('Dates')
    plt.ylabel('Price ($)')
    fig.autofmt_xdate()

    time_s = time_start.replace('-','')
    time_e = time_end.replace('-','')

    if not os.path.exists(output_dir):
        logger.info(f'OUTPUT DIRECTORY DOES NOT EXIST, CREATING: {output_dir}')
        os.mkdir(output_dir)

    output_file = f'{output_dir}/{ticker}_S{time_s}E{time_e}'
    logger.info(f'SAVING PLOT TO: {output_file}')
    fig.savefig(f'{output_file}')


if __name__ == "__main__":
    """
    examples:

    """
    
    parser = argparse.ArgumentParser('quant-MC-methods')

    # Required arguments
    parser.add_argument(
        "--action",
        help = "%(choices)s",
        type = str,
        choices = ['fetch_data', 'simulate', 'compare_times', 'compare_stocks', 'plot_ts'],
        required = True
    )
    
    # Optional arguments
    parser.add_argument(
        "--n",
        help = "N simulations (default: %(default)s)",
        type = int,
        required = False,
        default = 5000
    )

    parser.add_argument(
        "--start",
        help = "Starting date of data (default: %(default)s)",
        type = str,
        required = False,
        default = '2020-01-01'
    )

    parser.add_argument(
        "--end",
        help = "Ending date of data (default is today: %(default)s)",
        type = str,
        required = False,
        default = datetime.today().strftime('%Y-%m-%d')
    )

    parser.add_argument(
        "--ticker",
        help = "Ticker for analysis (default: %(default)s)",
        type = str,
        required = False,
        default = 'SPY'
    )

    parser.add_argument(
        "--stock2",
        help = "Ticker for comparison (default: %(default)s)",
        type = str,
        required = False,
        default = 'SPY'
    )

    parser.add_argument(
        "--output_dir",
        help = "Path of output directory for plots (default: %(default)s)",
        type = str,
        required = False,
        default = 'plots'
    )

    parser.add_argument(
        "--debug",
        help = "run logger in DEBUG mode (default: INFO)",
        required = False,
        action = "store_true"
    )
    
    args = parser.parse_args()

    # set up logger
    LOGGER_NAME = 'quant-MC-methods'
    logger_mode = "DEBUG" if args.debug else "INFO"
    logger = setup_logger(logger_mode, LOGGER_NAME)

    # main
    monte_carlo(args)