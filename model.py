# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error
# import joblib  # For saving the model

# # Function to preprocess data
# def preprocess_data(file_path):
#     df = pd.read_csv(file_path)
#     df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

#     # Handle null values
#     numeric_cols = df.select_dtypes(include=[np.number]).columns
#     for col in numeric_cols:
#         df[col].fillna(df[col].mean(), inplace=True)

#     # Remove outliers
#     Q1 = df['Price'].quantile(0.25)
#     Q3 = df['Price'].quantile(0.75)
#     IQR = Q3 - Q1
#     lower_bound = Q1 - (3 * IQR)
#     upper_bound = Q3 + (3 * IQR)
#     df = df[(df['Price'] > lower_bound) & (df['Price'] < upper_bound)]

#     # Create a target variable column
#     df['Future_Price'] = df['Price'].shift(-1)
#     df.dropna(inplace=True)  # Drop rows with no future price

#     return df

# # Load and preprocess Ethereum and Bitcoin data
# eth_data = preprocess_data(r"C:\Users\PIYUSH MHATRE\Desktop\CPP\Ethereum.csv")
# btc_data = preprocess_data(r"C:\Users\PIYUSH MHATRE\Desktop\CPP\Bitcoin.csv")

# # Train and predict function
# def train_and_predict(data, crypto_name):
#     # Split data into features (X) and target (y)
#     X = data[['Price']]
#     y = data['Future_Price']

#     # Split into training and validation sets
#     X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.1, random_state=2022)

#     # Scale the features
#     scaler = StandardScaler()
#     X_train_scaled = scaler.fit_transform(X_train)
#     X_valid_scaled = scaler.transform(X_valid)

#     # Train the Linear Regression model
#     model = LinearRegression()
#     model.fit(X_train_scaled, y_train)

#     # Save the scaler and model
#     joblib.dump(scaler, f"{crypto_name}_scaler.pkl")
#     joblib.dump(model, f"{crypto_name}_model.pkl")

#     # Make predictions and evaluate
#     y_pred = model.predict(X_valid_scaled)
#     mse = mean_squared_error(y_valid, y_pred)
#     print(f"{crypto_name} Mean Squared Error: {mse:.2f}")

#     # Predict next 20 days
#     last_known_price = data['Price'].iloc[-1]
#     predicted_prices = []

#     for _ in range(20):
#         last_known_price_scaled = scaler.transform([[last_known_price]])
#         next_price = model.predict(last_known_price_scaled)
#         predicted_prices.append(next_price[0])
#         last_known_price = next_price[0]

#     # Plot predictions
#     plt.figure(figsize=(10, 5))
#     plt.plot(range(1, 21), predicted_prices, marker='o')
#     plt.title(f'Predicted {crypto_name} Prices for the Next 20 Days')
#     plt.xlabel('Days')
#     plt.ylabel('Price')
#     plt.grid()
#     plt.show()

# # Train and predict for both Ethereum and Bitcoin
# train_and_predict(eth_data, 'Ethereum')
# train_and_predict(btc_data, 'Bitcoin')