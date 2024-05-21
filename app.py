import pandas as pd
import yfinance as yf
import subprocess
import webbrowser
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def get_live_indices_prices():
    try:
        # Ticker symbols for Nifty and Bank Nifty indices
        nifty_symbol = "^NSEI"
        banknifty_symbol = "^NSEBANK"
        
        # Fetch data for both indices
        nifty_data = yf.Ticker(nifty_symbol)
        banknifty_data = yf.Ticker(banknifty_symbol)
        
        # Get the live prices (last trade prices) for both indices
        nifty_price = round(nifty_data.history(period="1d")["Close"][0], 2)
        banknifty_price = round(banknifty_data.history(period="1d")["Close"][0], 2)

        # Calculate percentage change
        nifty_change = round(((nifty_price - nifty_data.history(period="1d")["Open"][0]) / nifty_data.history(period="1d")["Open"][0]) * 100, 2)
        banknifty_change = round(((banknifty_price - banknifty_data.history(period="1d")["Open"][0]) / banknifty_data.history(period="1d")["Open"][0]) * 100, 2)

        return nifty_price, banknifty_price, nifty_change, banknifty_change
    except Exception as e:
        print(f"Error fetching indices prices: {e}")
        return None, None, None, None

def read_csv_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def format_table_data(df):
    if df is not None:
        # Convert DataFrame to HTML table
        table_html = df.to_html(index=False)
        return table_html
    else:
        return None

@app.route('/')
def index():
    # Fetch live indices prices
    nifty_price, banknifty_price, nifty_change, banknifty_change = get_live_indices_prices()
    
    # Read data from CSV files
    
    top_gainers_df = read_csv_data("top_gainers.csv")
    top_losers_df = read_csv_data("top_losers.csv")
    nifty_stocks_df = read_csv_data("nifty_stocks.csv")
    breakout_stocks_df = read_csv_data("breakout_stocks.csv")

    # Format data for display on the webpage
    top_gainers_table = format_table_data(top_gainers_df)
    top_losers_table = format_table_data(top_losers_df)
    nifty_stocks_table = format_table_data(nifty_stocks_df)
    
    if breakout_stocks_df is not None:
        breakout_stocks = breakout_stocks_df[['Stock Name', 'Price', 'Volume']].values.tolist()
    else:
        breakout_stocks = []

    # Render the HTML template with the stock data
    return render_template('index.html', 
                           nifty_price=nifty_price,
                           banknifty_price=banknifty_price,
                           nifty_change=nifty_change,
                           banknifty_change=banknifty_change,
                           top_gainers=top_gainers_table, 
                           top_losers=top_losers_table, 
                           nifty_stocks=nifty_stocks_table,
                           breakout_stocks=breakout_stocks)

@app.route('/get_live_prices')
def get_live_prices():
    nifty_price, banknifty_price, nifty_change, banknifty_change = get_live_indices_prices()
    if nifty_price is not None and banknifty_price is not None:
        return jsonify({"nifty_price": nifty_price, "banknifty_price": banknifty_price, "nifty_change": nifty_change, "banknifty_change": banknifty_change})
    else:
        return jsonify({"error": "Failed to retrieve indices prices"})
    
@app.route('/stock-prediction')
def run_stock_prediction():
    # Run your app.py script
    subprocess.Popen(["python", "D:\\stock\\predict\\app.py"])
    return 'Stock prediction started!'    

if __name__ == '__main__':
    app.run(debug=True)

    webbrowser.open('http://127.0.0.1:5000/stock-prediction')