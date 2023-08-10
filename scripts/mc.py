
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
        simulate(args.ticker, args.start, args.end, args.time, args.output_dir)
    elif args.action == 'compare_times':
        compare_times()
    elif args.action == 'compare_stocks':
        compare_stocks()




def fetch_data(ticker, time_start, time_end, calc_mu_std=True):
    """
    Tests API connection
    Fetches data from yfinance, calculates a return column, and returns df, mu and std by default
    """
    # fetch data
    data = yf.Ticker(ticker)
    logger.info(f"FETCHING DATA: {ticker} from {time_start} to {time_end}")
    df = data.history(start=time_start, end=time_end, rounding=True)
    logger.debug(f"FETCHED DATA: {ticker} - df shape: {df.shape}")
    df['return'] = (df['Close'] - df['Open']) / df['Open']
    
    if df.shape[0] == 0:
        logger.info(f"FETCH UNSUCCESSFUL - SHAPE: {df.shape}")
        return
    else:
        logger.info(f"FETCHED SUCCESSFULLY - SHAPE: {df.shape}")

    # calculate mu std
    mu, std = ( (df.iloc[-1]['Close'] - df.iloc[0]['Close']) / df.iloc[0]['Close'] , df['return'].std() ) if calc_mu_std else (None, None)

    if mu != None:
        total_time = len(df)
        logger.info(f"From {str(df.index[0])[:10]} to {str(df.index[-1])[:10]}:") # fix with regex?
        logger.info(f"  Average return in {total_time} market days is {100*mu:.3f}%")
        logger.info(f"  Standard deviation of returns during this time period is {std:.3f}")

    return (df, (mu, std))


def plot_ts(ticker, time_start, time_end, output_dir): # , plot_returns=True
    """
    Fetches data and plots time series of a ticker in a specific time frame
    Stores plots in output_dir in format {ticker}_S{YYYYMMDD}E{YYYYMMDD}.png
    """
    logger.info(f"PLOTTING TICKER: {ticker} from {time_start} to {time_end}")
    df = fetch_data(ticker, time_start, time_end, calc_mu_std=False)[0]
    logger.debug(f"FETCHED DATA: {ticker} - df shape: {df.shape}")

    # Creating plots
    logger.info("")
    logger.info(f"TICKER: {ticker}")
    logger.info(f"Start price: ${df.iloc[0]['Close']} ({time_start})")
    logger.info(f"End price: ${df.iloc[-1]['Close']} ({time_end})")
    logger.info("---------------------------------------------")
    fig, axes = plt.subplots(1, 2, figsize=(12,4))
    plt.suptitle(f"{ticker} from {time_start} to {time_end}")

    # Plot time series
    axes[0].plot(df['Close'])
    axes[0].set_xlabel("Dates")
    axes[0].set_ylabel("Price (USD)")
    axes[0].set_title(f"Time series")
    fig.autofmt_xdate()

    # Plot histogram of returns
    axes[1].hist(df['return'], bins='auto')
    axes[1].set_xlabel("Returns")
    axes[1].set_ylabel("Frequency")
    axes[1].set_title("Histogram of returns")
    
    ## histogram density = True
    locs = axes[1].get_yticks() 
    tick_labels = [f"{loc/len(df['return']):.3f}" for loc in locs]
    axes[1].set_yticks(locs);
    axes[1].set_yticklabels(tick_labels);

    # Storing plots
    time_s = time_start.replace('-','')
    time_e = time_end.replace('-','')

    if not os.path.exists(output_dir):
        logger.info(f'OUTPUT DIRECTORY DOES NOT EXIST, CREATING: {output_dir}')
        os.mkdir(output_dir)

    output_file = f'{output_dir}/{ticker}_S{time_s}E{time_e}' # change output file path here
    logger.info(f'SAVING PLOT TO: {output_file}')
    fig.savefig(f'{output_file}')


def simulate(ticker, time_start, time_end, time, output_dir):
    """
    
    """
    df, (mu, sigma) = fetch_data(ticker, time_start, time_end)
    S0 = df.iloc[-1]['Close']
    muS = mu/len(df)



if __name__ == "__main__":
    """
    examples:
    
    python scripts/mc.py --action fetch_data --ticker TSM 
    python scripts/mc.py --action plot_ts --start 2023-01-31 --ticker LMND

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
        "--time",
        help = "Simulate n days ahead (default: %(default)s)",
        type = int,
        required = False,
        default = 252
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