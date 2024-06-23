from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import xgboost as xgb


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction')
def render_prediction():
    return render_template('prediction.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Convert the input data to the appropriate data types
    for key in data:
        if key in ['Item_Identifier', 'Item_Fat_Content', 'Item_Type', 'Outlet_Identifier', 'Outlet_Establishment_Year', 'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type']:
            data[key] = int(data[key])
        else:
            data[key] = float(data[key])

    df = pd.DataFrame([data], columns=[
        'Item_Identifier', 'Item_Weight', 'Item_Fat_Content', 'Item_Visibility',
        'Item_Type', 'Item_MRP', 'Outlet_Identifier', 'Outlet_Establishment_Year',
        'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type'])

    model = xgb.XGBRegressor()
    model.load_model('C:\\Users\\User\\Downloads\\Big Mart Sales prediction project\\Big Mart Sales prediction project\\BIG MART SALES PREDICTION\\bigmartsales_prediciton_ui\\sales predict\\xgb_model.bin')


    prediction = model.predict(df)
    result = float(prediction[0])

    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)