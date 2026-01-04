import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

data = {
    'Area': [800, 900, 1000, 1100, 1200, 1300, 1400],
    'Bedrooms': [1, 2, 2, 3, 3, 3, 4],
    'Age': [20, 15, 10, 8, 5, 3, 1],
    'Price': [30, 35, 40, 50, 55, 65, 75]
}

df = pd.DataFrame(data)

X = df[['Area', 'Bedrooms', 'Age']]
y = df['Price']

model = LinearRegression()
model.fit(X, y)

pickle.dump(model, open('model.pkl', 'wb'))
print("Model trained and saved successfully")