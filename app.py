from flask import Flask, render_template, send_file
import joblib
import matplotlib.pyplot as plt
import io
import pandas as pd  # Make sure pandas is imported

# Initialize Flask app
app = Flask(__name__)

# Load Ethereum model and scaler
eth_model = joblib.load("C:\\Users\\PIYUSH MHATRE\\Desktop\\CPE API\\cpe piyush\\temp (2)\\temp\\Ethereum_model.pkl")
eth_scaler = joblib.load("C:\\Users\\PIYUSH MHATRE\\Desktop\\CPE API\\cpe piyush\\temp (2)\\temp\\Ethereum_scaler.pkl")

# Load Bitcoin model and scaler
btc_model = joblib.load("C:\\Users\\PIYUSH MHATRE\\Desktop\\CPE API\\cpe piyush\\temp (2)\\temp\\Bitcoin_model.pkl")
btc_scaler = joblib.load("C:\\Users\\PIYUSH MHATRE\\Desktop\\CPE API\\cpe piyush\\temp (2)\\temp\\Bitcoin_scaler.pkl")

# Helper function to generate prediction graphs
def generate_prediction_graph(crypto_name, model, scaler, data):
    # Get the last known price from the dataset for the prediction
    last_known_price = data['Price'].iloc[-1]  # Use the last known price

    predicted_prices = []
    for _ in range(20):
        last_known_price_scaled = scaler.transform([[last_known_price]])
        next_price = model.predict(last_known_price_scaled)
        predicted_prices.append(next_price[0])
        last_known_price = next_price[0]

    # Plot predictions
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, 21), predicted_prices, marker='o')
    plt.title(f'Predicted {crypto_name} Prices for the Next 20 Days')
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.grid()

    # Save the plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return img

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict/<crypto_name>', methods=['GET'])
def predict(crypto_name):
    if crypto_name == 'Ethereum':
        # Load the Ethereum data (assuming it is preprocessed)
        eth_data = pd.read_csv("C:\\Users\\PIYUSH MHATRE\\Desktop\\CPE API\\cpe piyush\\temp (2)\\temp\\Ethereum.csv")  # Adjust with actual path if needed
        img = generate_prediction_graph('Ethereum', eth_model, eth_scaler, eth_data)
    elif crypto_name == 'Bitcoin':
        # Load the Bitcoin data (assuming it is preprocessed)
        btc_data = pd.read_csv("C:\\Users\\PIYUSH MHATRE\\Desktop\\CPE API\\cpe piyush\\temp (2)\\temp\\bitcoin (2).csv")  # Adjust with actual path if needed
        img = generate_prediction_graph('Bitcoin', btc_model, btc_scaler, btc_data)
    else:
        return "Invalid cryptocurrency", 400
    
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
