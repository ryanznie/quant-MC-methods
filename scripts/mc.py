
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime
import os
import argparse
from argparse import RawTextHelpFormatter
from utils import setup_logger


def monte_carlo(args):
    """
    Main
    CLI tool for stock price predictions using Monte Carlo methods
    """

    # For consistent naming
    ticker = args.ticker.upper()
    ticker2 = args.ticker2.upper()

    # actions
    logger.info("")
    if args.action == 'fetch_data':
        fetch_data(ticker, args.start, args.end)
    elif args.action == 'plot_ts':
        plot_ts(ticker, args.start, args.end, args.output_dir, args.no_returns_plot)
    elif args.action == 'simulate':
        simulate(ticker, args.num_sim, args.start, args.end, args.time, args.output_dir)
    elif args.action == 'compare_stocks':
        compare_stocks(ticker, ticker2, args.num_sim, args.start, args.end, args.time, args.output_dir)


def fetch_data(ticker, time_start, time_end, calc_mu_std=True):
    """
    Tests API connection
    Fetches data from yfinance, calculates a return column, and returns df, mu and std by default
    """
    
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


def plot_ts(ticker, time_start, time_end, output_dir, no_returns_plot):
    """
    Fetches data and plots time series of a ticker in a specific time frame
    OPTIONAL: plot histogram of returns, default plot returns
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

    if not no_returns_plot:
        fig, axes = plt.subplots(1, 2, figsize=(12,4))
        plt.suptitle(f"{ticker} from {time_start} to {time_end}")

        # Plot time series
        axes[0].plot(df['Close'])
        axes[0].set_xlabel("Dates")
        axes[0].set_ylabel("Price (USD)")
        axes[0].set_title(f"Time series")
        
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

        fig.autofmt_xdate()

    else:
        # Plot time series
        fig = plt.figure()
        plt.plot(df['Close'])
        plt.xlabel("Dates")
        plt.ylabel("Price (USD)")
        plt.title(f"{ticker} from {time_start} to {time_end}")
        fig.autofmt_xdate()
        
    # Storing plots
    time_s = time_start.replace('-','')
    time_e = time_end.replace('-','')

    if not os.path.exists(output_dir):
        logger.info(f'OUTPUT DIRECTORY DOES NOT EXIST, CREATING: {output_dir}')
        os.mkdir(output_dir)

    output_file = f'{output_dir}/{ticker}_S{time_s}E{time_e}' # change output file path here
    logger.info(f'SAVING PLOT TO: {output_file}')
    fig.savefig(f'{output_file}')


def simulate(ticker, num_sim, time_start, time_end, time, output_dir, plot=True):
    """
    Fetches data, and simulates {time} days into the future {num_sim} times using Monte Carlo methods
    Plots and store results in {output_dir} (default: plots)
    """
    ### PLOT ORIGINAL TS, open plot files for people?
    df, (mu, sigma) = fetch_data(ticker, time_start, time_end)
    S0 = df.iloc[-1]['Close']
    muS = mu/len(df)

    final_points = []

    logger.info("")
    logger.info("---------------------------------------------")
    logger.info(f"Simulating {ticker} {time} days into the future {num_sim} times...")

    # MC simulate num_sim times
    for sim in range(num_sim):
        S_pos = [S0]
        Z = np.random.normal(0,1, size = time)
        for t in range(0, time):
            S_pos.append(S_pos[t] + S_pos[t]*(muS + sigma*Z[t]))
        final_points.append(S_pos[-1])
    logger.info("Simulations completed")

    # Stops plotting
    if not plot:
        logger.debug("Not plotting, returning final_points")
        return final_points
    
    # Descriptive statistics for ending points
    logger.info("")
    logger.info(f"Calculating descriptive statistics...")
    average = np.mean(final_points)
    median = np.percentile(final_points, 50)
    twentyfive = np.percentile(final_points, 25)
    seventyfive = np.percentile(final_points, 75)

    logger.info(f"  Average ending price: ${average:.2f}  ({(100*(average-S0)/S0):.2f}%)")
    logger.info(f"  Median ending price: ${median:.2f}  ({(100*(median-S0)/S0):.2f}%)")
    logger.info(f"  25th percentile of ending price: ${twentyfive:.2f}  ({(100*(twentyfive-S0)/S0):.2f}%)")
    logger.info(f"  75th percentile of ending price: ${seventyfive:.2f}  ({(100*(seventyfive-S0)/S0):.2f}%)")

    if not os.path.exists(output_dir):
        logger.info(f'OUTPUT DIRECTORY DOES NOT EXIST, CREATING: {output_dir}')
        os.mkdir(output_dir)

    # plotting
    fig, axes = plt.subplots(1, 2, figsize=(12,4))
    fig.suptitle(f"{num_sim} Simulations Result: {ticker} ({time} days)", fontsize=18, y = 1)

    ## plot histogram
    axes[0].hist(final_points, bins='auto', density=False)
    axes[0].set_xlabel("Ending Price")
    axes[0].set_ylabel("Frequency")
    axes[0].set_title("Histogram of future prices")

    ## plot boxplot
    sns.boxplot(data=final_points, orient="h", ax=axes[1])
    plt.title("Boxplot of future prices")
    plt.xlabel("Price in USD")
    
    output_file = f'{output_dir}/{ticker}_sim{time}D' # change output file path here
    logger.info(f'SAVING PLOT TO: {output_file}')
    fig.savefig(f'{output_file}')


def compare_stocks(ticker, ticker2, num_sim, start, end, time, output_dir):
    """
    Calls simulate() on two stocks and plot both histograms next to each other
    """
    end_points1 = simulate(ticker, num_sim, start, end, time, output_dir, plot=False)
    end_points2 = simulate(ticker2, num_sim, start, end, time, output_dir, plot=False)
    
    # plotting
    fig, axes = plt.subplots(1, 2, figsize=(12,4))
    fig.suptitle(f"Histogram of future prices ({time} days): {ticker} vs {ticker2}", fontsize=18, y = 1)

    ## plot histogram: ticker
    axes[0].hist(end_points1, bins='auto', density=False)
    axes[0].set_xlabel("Ending Price")
    axes[0].set_ylabel("Frequency")
    axes[0].set_title(f"{ticker}")

    ## plot histogram: ticker2
    axes[1].hist(end_points2, bins='auto', density=False)
    axes[1].set_xlabel("Ending Price")
    axes[1].set_ylabel("Frequency")
    axes[1].set_title(f"{ticker2}")

    if not os.path.exists(output_dir):
        logger.info(f'OUTPUT DIRECTORY DOES NOT EXIST, CREATING: {output_dir}')
        os.mkdir(output_dir)

    output_file = f'{output_dir}/{ticker}_comp_{ticker2}' # change output file path here
    logger.info(f'SAVING PLOT TO: {output_file}')
    fig.savefig(f'{output_file}')


if __name__ == "__main__":
    """
    examples:
    
    python scripts/mc.py --action fetch_data --ticker TSM 
    python scripts/mc.py --action plot_ts --start 2023-01-31 --ticker LMND
    python scripts/mc.py --action plot_ts --start 2023-01-31 --end 2023-05-02 --ticker CVS --no_returns_plot
    python scripts/mc.py --action simulate --num_sim 6000 --start 2023-01-31 --ticker PYPL --time 500
    python scripts/mc.py --action simulate -n 6000 --ticker TMUS --time 500
    python scripts/mc.py --action compare_stocks -n 6000 --ticker MA --ticker2 V

    
    ### FUTURE IMPLEMENTATIONS? 
    action -> create plot objects -> organize() function at the end to plot
    i.e plotting happens outside the function
    """
    
    parser = argparse.ArgumentParser('quant-MC-methods', formatter_class=RawTextHelpFormatter)

    # Required arguments
    parser.add_argument(
        "--action",
        help = 
        """
        fetch_data: Fetches data from yfinance API
        plot_ts: Plots time series and histogram of returns
        simulate: 
        compare_stocks
        """,
        type = str,
        choices = ['fetch_data', 'plot_ts', 'simulate', 'compare_stocks'],
        required = True
    )
    
    # Optional arguments
    parser.add_argument(
        "--num_sim", 
        "-n",
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
        metavar = "START TIME",
        type = str,
        required = False,
        default = '2020-01-01'
    )

    parser.add_argument(
        "--end",
        help = "Ending date of data (default is today: %(default)s)",
        metavar = "END TIME",
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
        "--ticker2",
        help = "Ticker for comparison (default: %(default)s)",
        type = str,
        required = False,
        default = 'SPY'
    )

    parser.add_argument(
        "--output_dir",
        help = "Path of output directory for plots (default: %(default)s)",
        metavar = "PATH",
        type = str,
        required = False,
        default = 'plots'
    )

    parser.add_argument(
        '--no_returns_plot',
        help = "Do not plot returns in plot_ts (default: plots returns)",
        required = False,
        action = "store_true"
    )

    parser.add_argument(
        "--debug",
        help = "Run logger in DEBUG mode (default: INFO)",
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