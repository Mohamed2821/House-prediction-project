import os
print(os.listdir())
print(os.listdir("templates"))
from flask import Flask, render_template, request
import pickle
import os
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

MODEL_FILE = "model.pkl"

# Train model if not exists
def train_model():
    data = {
        'Area': [800, 900, 1000, 1100, 1200, 1300, 1400],
        'Bedrooms': [1, 2, 2, 3, 3, 3, 4],
        'Age': [20, 15, 10, 8, 5, 3, 1],
        'Price': [30, 35, 40, 50, 55, 65, 75]  # Price in Lakhs (INR)
    }

    df = pd.DataFrame(data)
    X = df[['Area', 'Bedrooms', 'Age']]
    y = df['Price']

    model = LinearRegression()
    model.fit(X, y)

    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)

    return model

# Load or train model
if os.path.exists(MODEL_FILE):
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)
else:
    model = train_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        area = float(request.form['area'])
        bedrooms = int(request.form['bedrooms'])
        age = int(request.form['age'])
        currency = request.form['currency']

        prediction = model.predict([[area, bedrooms, age]])[0]

        # Currency conversion
        if currency == "USD":
            prediction *= 0.012
            symbol = "$"
        elif currency == "EUR":
            prediction *= 0.011
            symbol = "€"
        else:
            symbol = "₹"

        prediction = round(prediction, 2)

        return render_template(
            'index.html',
            prediction=prediction,
            symbol=symbol
        )

    except Exception as e:
        return render_template(
            'index.html',
            error="Invalid input. Please enter valid values."
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
