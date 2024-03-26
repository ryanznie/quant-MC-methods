from flask import Flask, request, jsonify, render_template
from logger_setup import logger
from app_utils import fetch_data, simulate
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import os

app = Flask(__name__)

# Specify the folder from which Flask will serve static files
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/plots/<ticker>/<days>', methods=['POST'])
def get_plots(ticker, days):
    ticker = request.json.get('ticker')
    days = request.json.get('days')

    # Validation
    if not ticker:
        return jsonify({'error': 'Ticker not provided'}), 400
    if not days:
        return jsonify({'error': 'Day not provided'}), 400
    
    data = fetch_data(ticker, time_start='2019-01-01', time_end='2024-01-01')  # Fetch 5-year historical data
    if data is None:
        return jsonify({'error': 'Ticker cannot be found on yFinance'}), 404
    
    final_points, num_sim = simulate(data, days, ticker) # return image path too
    
    # Create a static dir if it does not already exist
    if not os.path.exists('static'):
        logger.info('OUTPUT DIRECTORY DOES NOT EXIST, CREATING: static')
        os.mkdir('static')

    # Plotting
    fig, axes = plt.subplots(2, 2, figsize=(12,8))  # Create subplot for 5-year historical data
    plt.subplots_adjust(hspace=0.5, wspace=0.2)
    fig.suptitle("Simulated {} times: {} ({} days ahead) using 5Y historical".format(num_sim, ticker.upper(), days), fontsize=18, y=1)

    # Plot histogram
    axes[0, 0].hist(final_points, bins='auto', density=False)
    axes[0, 0].set_xlabel("Ending Price")
    axes[0, 0].set_ylabel("Frequency")
    axes[0, 0].set_title("Histogram of future prices")

    # Plot boxplot
    sns.boxplot(data=final_points, orient="h", ax=axes[0, 1])
    axes[0, 1].set_title("Boxplot of future prices")
    axes[0, 1].set_xlabel("Price in USD")

    # Plot 5-year historical data
    df = data[0]
    axes[1, 0].plot(df.index, df['Close'], label="Close Price")
    axes[1, 0].set_title("5-year Historical Data")
    axes[1, 0].set_xlabel("Date")
    axes[1, 0].set_ylabel("Price")
    axes[1, 0].legend()

    # Table with relevant stock data
    axes[1, 1].axis('off')  # Disable axis for table
    table_data = [
        ['Open', df.iloc[-1]['Open']], 
        ['Close', df.iloc[-1]['Close']], 
        ['High', df.iloc[-1]['High']], 
        ['Low', df.iloc[-1]['Low']], 
        ['Volume', df.iloc[-1]['Volume']],
        ['Previous Close', df.iloc[-2]['Close']],
        ['52 Week High', df['High'].max()],
        ['52 Week Low', df['Low'].min()],
    ]
    axes[1, 1].table(cellText=table_data, loc='center')

    plot_url = 'static/{}_sim{}D.png'.format(ticker, days)  # Add .png extension
    logger.info('SAVING PLOT TO: {}'.format(plot_url))
    fig.savefig(plot_url)
    plt.close(fig)

    # Return render_template('plots.html', image_path=image_path)
    return jsonify({
                    'image_url': plot_url,
                    'ticker': ticker,
                    'date': days
                    }), 200

if __name__ == '__main__':
    app.run(debug=True)
