from flask import Flask, render_template, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

app = Flask(__name__)


def predict_stock_price(stock_name):
    try:
        
        data = pd.read_csv(f'{stock_name}.csv')
    except FileNotFoundError:
        return None, None, "Error: Stock data not found."

    
    data.columns = data.columns.str.strip()

    if len(data) < 2:
        return None, None, "Error: Insufficient data for prediction."

    
    X = data[['OPEN', 'HIGH', 'LOW', 'PREV. CLOSE']]
    y = data['close']

    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    
    model = LinearRegression()

    try:
        
        model.fit(X_train, y_train)

        
        y_pred = model.predict(X_test)

       
        mse = mean_squared_error(y_test, y_pred)

        
        last_data_point = data.iloc[-1][['OPEN', 'HIGH', 'LOW', 'PREV. CLOSE']].values.reshape(1, -1)
        future_price = model.predict(last_data_point)

        
        close_price_H2 = data.iloc[1]['close']

        return future_price[0], close_price_H2, None
    except Exception as e:
        return None, None, f"Error: Model training or prediction failed - {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_price = None
    close_price_H2 = None
    total_price = None
    error_message = None

    if request.method == 'POST':
        stock_name = request.form['stock_name']
        predicted_price, close_price_H2, error_message = predict_stock_price(stock_name)
        
        
        if predicted_price is not None and close_price_H2 is not None:
            total_price = predicted_price + close_price_H2

    return render_template('index.html', predicted_price=predicted_price, close_price_H2=close_price_H2, total_price=total_price, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
