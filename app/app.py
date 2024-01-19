from flask import Flask, request, jsonify
from app_utils import fetch_data#, plot_data

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

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
    result = data[1]

    return jsonify({'image_url': result,
                    'date': days}
                    ), 200


if __name__ == '__main__':
    app.run(debug=True)