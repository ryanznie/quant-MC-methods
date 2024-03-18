from flask import Flask, request, jsonify, render_template
from logger_setup import logger
from app_utils import fetch_data, simulate#, plot_data
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plots/<ticker>/<days>', methods=['POST'])
def get_plots(ticker, days):
    ticker = request.json.get('ticker')
    days = request.json.get('days')

    # Validation
    if not ticker:
        return jsonify({'error': 'Ticker not provided'}), 400
    if not days:
        return jsonify({'error': 'Day not provided'}), 400
    
    data = fetch_data(ticker, time_start='2020-01-01', time_end='2020-12-31')
    if data is None:
        return jsonify({'error': 'Ticker cannot be found on yFinance'}), 400
    
    final_points, num_sim = simulate(data, days, ticker) # return image path too
    
    # create a static dir if it does not already exist

    if not os.path.exists('static'):
        logger.info(f'OUTPUT DIRECTORY DOES NOT EXIST, CREATING: static')
        os.mkdir(output_dir)

    # plotting
    fig, axes = plt.subplots(1, 2, figsize=(12,4))
    fig.suptitle(f"Simulated {num_sim} times...: {ticker} ({days} days ahead)", fontsize=18, y = 1)

    ## plot histogram
    axes[0].hist(final_points, bins='auto', density=False)
    axes[0].set_xlabel("Ending Price")
    axes[0].set_ylabel("Frequency")
    axes[0].set_title("Histogram of future prices")

    ## plot boxplot
    sns.boxplot(data=final_points, orient="h", ax=axes[1])
    plt.title("Boxplot of future prices")
    plt.xlabel("Price in USD")
    
    plot_url = f'static/{ticker}_sim{days}D' # change output file path here
    logger.info(f'SAVING PLOT TO: {plot_url}')
    fig.savefig(f'{plot_url}')
    plt.close(fig)

    #return render_template('plots.html', image_path=image_path)
    return jsonify({
                    'image_url': plot_url,
                    'ticker': ticker,
                    'date': days
                    }), 200


if __name__ == '__main__':
    app.run(debug=True)