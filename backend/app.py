# app.py
from flask import Flask, jsonify, request
from charts import create_candlestick_chart
from predictions import get_lstm_predictions
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/candlestick-chart', methods=['GET'])
def candlestick_chart():
    # Get stock symbol from query parameter (default: AAPL)
    stock_symbol = request.args.get('symbol', 'AAPL')
    candlestick_data = create_candlestick_chart(stock_symbol)
    return jsonify(candlestick_data)

@app.route('/combined-chart', methods=['GET'])
def combined_chart():
    stock_symbol = request.args.get('symbol', 'AAPL')
    
    # Generate candlestick data
    candlestick_data = create_candlestick_chart(stock_symbol)
    if "error" in candlestick_data:
        return jsonify(candlestick_data)
    
    # Get LSTM predictions
    lstm_data = get_lstm_predictions(stock_symbol)
    if "error" in lstm_data:
        return jsonify(lstm_data)
    
    # Combine both datasets into one
    combined_data = candlestick_data
    combined_data["data"].append({
        "x": lstm_data["dates"],
        "y": lstm_data["predictions"],
        "type": "scatter",
        "mode": "lines",
        "name": "LSTM Predictions",
        "line": {"color": "blue", "width": 2}
    })
    return jsonify(combined_data)

if __name__ == '__main__':
    app.run(debug=True)

