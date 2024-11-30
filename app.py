from flask import Flask, request
import pandas as pd
import os

app = Flask(__name__)

# Path to save the Excel file
FILEPATH = r"C:\Users\vijen\Desktop\TRADE\trading_data.xlsx"

# Ensure the directory exists, and create Excel file if it doesn't exist
def create_excel_file():
    folder_path = os.path.dirname(FILEPATH)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Create the folder if it doesn't exist

    if not os.path.exists(FILEPATH):
        # Create a default DataFrame with columns for the Excel file
        df = pd.DataFrame(columns=["Timestamp", "Symbol", "Price", "Volume"])
        df.to_excel(FILEPATH, index=False)
        print(f"Excel file created at {FILEPATH}")

# Create the Excel file if it doesn't exist
create_excel_file()

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        data = request.json
        
        # Extract data from the TradingView alert
        timestamp = data.get("time")
        symbol = data.get("symbol")
        price = data.get("price")
        volume = data.get("volume", "N/A")  # Default volume is "N/A" if not provided

        # Append the data to the Excel file
        df = pd.read_excel(FILEPATH)
        new_row = {"Timestamp": timestamp, "Symbol": symbol, "Price": price, "Volume": volume}
        df = df.append(new_row, ignore_index=True)
        df.to_excel(FILEPATH, index=False)

        return "Data received and written to Excel.", 200
    return "Webhook running."

if __name__ == "__main__":
    app.run(debug=False)
