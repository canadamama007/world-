import sys
try:
    import streamlit as st
except ModuleNotFoundError:
    sys.exit("\nERROR: Streamlit is not installed. Run 'pip install streamlit' and try again.\n")

import pandas as pd
from sklearn.linear_model import LinearRegression

# Simulated Ontario housing data
data = {
    'square_feet': [1200, 1500, 1800, 2200, 2600, 3000],
    'bedrooms': [2, 3, 3, 4, 4, 5],
    'bathrooms': [1, 2, 2, 3, 3, 4],
    'city': ['Toronto', 'Ottawa', 'Toronto', 'Mississauga', 'Ottawa', 'Toronto'],
    'price': [550000, 600000, 750000, 850000, 900000, 1200000]
}

df = pd.DataFrame(data)
df = pd.get_dummies(df, columns=['city'])

X = df.drop('price', axis=1)
y = df['price']

model = LinearRegression()
model.fit(X, y)

# UI
st.title("Ontario House Price Predictor 🏡")

sqft = st.number_input("Enter square footage", min_value=500, max_value=5000, value=2000)
bedrooms = st.selectbox("Number of bedrooms", [1, 2, 3, 4, 5])
bathrooms = st.selectbox("Number of bathrooms", [1, 2, 3, 4])
city = st.selectbox("Select city", ['Toronto', 'Ottawa', 'Mississauga'])

# Create input DataFrame with all dummy variables
input_data = {
    'square_feet': sqft,
    'bedrooms': bedrooms,
    'bathrooms': bathrooms,
    'city_Mississauga': 1 if city == 'Mississauga' else 0,
    'city_Ottawa': 1 if city == 'Ottawa' else 0,
    'city_Toronto': 1 if city == 'Toronto' else 0
}

input_df = pd.DataFrame([input_data])[X.columns]

if st.button("Predict Price"):
    prediction = model.predict(input_df)[0]
    st.success(f"Estimated House Price: ${prediction:,.0f}")
