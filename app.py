from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/api/history')
def get_history():
    symbol = request.args.get('symbol')
    period = request.args.get('period', '5y')
    interval = request.args.get('interval', '1d')
    if not symbol:
        return jsonify({'error': 'No symbol provided'}), 400
    
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, interval=interval)
    
    if hist.empty:
        return jsonify({'error': 'No data found for symbol'}), 404

    # The financial chart plugin expects time data in milliseconds
    hist.index = hist.index.astype('int64') // 10**6    
    # Format data for candlestick chart
    data = [
        {
            "x": idx,
            "o": row["Open"],
            "h": row["High"],
            "l": row["Low"],
            "c": row["Close"]
        }
        for idx, row in hist.iterrows()
    ]
    
    return jsonify({'symbol': symbol, 'data': data})

if __name__ == '__main__':
    app.run(port=5000) 