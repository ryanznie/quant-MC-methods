import yfinance as yf
import pandas as pd
import logging
import logging.config
import sys


enable_debug_logging = True

logging.config.fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

if enable_debug_logging:
    logger.setLevel(logging.DEBUG)


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
        return
    else:
        logger.info(f"FETCHED SUCCESSFULLY - SHAPE: {df.shape}")

    # calculate mu std
    mu, std = ( (df.iloc[-1]['Close'] - df.iloc[0]['Close']) / df.iloc[0]['Close'] , df['return'].std() )

    if mu != None:
        total_time = len(df)
        logger.info(f"From {str(df.index[0])[:10]} to {str(df.index[-1])[:10]}:") # fix with regex?
        logger.info(f"  Average return in {total_time} market days is {100*mu:.3f}%")
        logger.info(f"  Standard deviation of returns during this time period is {std:.3f}")

    return (df, (mu, std))