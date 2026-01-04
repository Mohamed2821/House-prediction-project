from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    area = float(request.form['area'])
    bedrooms = int(request.form['bedrooms'])
    age = int(request.form['age'])
    currency = request.form['currency']

    prediction = model.predict([[area, bedrooms, age]])[0]

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

if __name__ == "__main__":
    app.run(debug=True)