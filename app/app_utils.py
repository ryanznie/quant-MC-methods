import yfinance as yf
import pandas as pd
import numpy as np
from logger_setup import logger


def fetch_data(ticker, time_start, time_end):
    """
    Fetches data from yfinance, calculates a return column, and returns df, mu and std by default
    """
    
    data = yf.Ticker(ticker)
    logger.info(f"FETCHING DATA: {ticker} from {time_start} to {time_end}")
    df = data.history(start=time_start, end=time_end, rounding=True)
    logger.debug(f"FETCHED DATA: {ticker} - df shape: {df.shape}")
    df['return'] = (df['Close'] - df['Open']) / df['Open']
    
    if df.shape[0] == 0:
        logger.info(f"FETCH UNSUCCESSFUL - SHAPE: {df.shape}")
        return None
    else:
        logger.info(f"FETCHED SUCCESSFULLY - SHAPE: {df.shape}")

    # calculate mu std
    mu, std = ( (df.iloc[-1]['Close'] - df.iloc[0]['Close']) / df.iloc[0]['Close'] , df['return'].std() )

    total_time = len(df)
    logger.info(f"From {str(df.index[0])[:10]} to {str(df.index[-1])[:10]}:") # fix with regex?
    logger.info(f"  Average return in {total_time} market days is {100*mu:.3f}%")
    logger.info(f"  Standard deviation of returns during this time period is {std:.3f}")

    return (df, (mu, std))


def simulate(data, time, ticker, num_sim=100):
    """
    MC simulates {time} days into the future {num_sim} times using Monte Carlo methods
    Plots and store results in {output_dir} (default: static)
    """
    df = data[0]
    mu, sigma = data[1]

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

    return final_points, num_sim

