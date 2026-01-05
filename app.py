from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model (SAFE METHOD)
model = joblib.load("model.joblib")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    if request.method == "POST":
        try:
            area = float(request.form["area"])
            bedrooms = int(request.form["bedrooms"])
            bathrooms = int(request.form["bathrooms"])

            features = np.array([[area, bedrooms, bathrooms]])
            prediction = round(model.predict(features)[0], 2)

        except Exception as e:
            prediction = "Invalid input"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
