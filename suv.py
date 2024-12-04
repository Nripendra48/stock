import pandas as pd
import yfinance as yf
import numpy as np

# Step 1: Accepting User Input for Investment Date and Amount
investment_date = input("Enter the date (YYYY-MM-DD): ")  # Only one day for calculation
investment_amount = float(input("Enter the total investment amount: "))

# Step 2: Load Stock Data from CSV
stocks_df = pd.read_csv('stocks.csv')  # Ensure 'stocks.csv' is in the same directory or provide the correct path
print("Stock Data Loaded: \n", stocks_df)

# Drop irrelevant columns (if any)
stocks_df = stocks_df[['Ticker', 'Weightage']]  # Keep only the relevant columns

# Clean up column names 
stocks_df.columns = stocks_df.columns.str.strip()

print(stocks_df)

# Step 3: Fetch Historical Data for Each Stock Using Yahoo Finance API
stock_symbols = stocks_df['Ticker'].tolist()
stock_weights = stocks_df['Weightage'].tolist()
print("Stock Symbols: ", stock_symbols)

# Create a dictionary to store the stock data
stock_data = {}

# Fetch stock data for each symbol
for stock in stock_symbols:
    try:
        # Modify ticker symbol for Indian stocks (append '.NS' for NSE, '.BO' for BSE)
        if stock.endswith("NS"):  # For NSE stocks
            ticker = stock
        elif stock.endswith("BO"):  # For BSE stocks
            ticker = stock
        else:  # Default case, assuming NSE by default
            ticker = stock + ".NS"  # Append .NS for NSE stocks
        
        # Fetch historical data for the specified date (single day)
        stock_data[stock] = yf.download(ticker, start=investment_date, end=investment_date)
    except Exception as e:
        print(f"Error downloading data for {stock}: {e}")
        stock_data[stock] = pd.DataFrame()  # Create empty data for this stock if error occurs

# Step 4: Calculate Number of Shares that can be Bought for Each Stock on the Given Day
result = []

# Loop for the specified single date
daily_result = {'Date': investment_date}

for stock, weight in zip(stock_symbols, stock_weights):
    # Calculate investment amount for this stock
    amount_to_invest = investment_amount * weight
    if not stock_data[stock].empty:
        try:
            open_price = stock_data[stock]['Open'].iloc[0].item()  # Extract scalar value
            close_price = stock_data[stock]['Close'].iloc[0].item()
            
            # Calculate shares to buy
            shares_to_buy_open = amount_to_invest / open_price if open_price > 0 else None
            shares_to_buy_close = amount_to_invest / close_price if close_price > 0 else None
            
            daily_result[f"{stock}_Shares_Open"] = shares_to_buy_open
            daily_result[f"{stock}_Shares_Close"] = shares_to_buy_close
        except ValueError:
            print(f"Error processing {stock}. Open/Close prices may be invalid.")
            daily_result[f"{stock}_Shares_Open"] = None
            daily_result[f"{stock}_Shares_Close"] = None
    else:
        daily_result[f"{stock}_Shares_Open"] = None
        daily_result[f"{stock}_Shares_Close"] = None


result.append(daily_result)

# Step 5: Write Results to Excel File
result_df = pd.DataFrame(result)

# Save with the investment date as the header in the Excel file
file_name = f"investment_result_{investment_date}.xlsx"
result_df.to_excel(file_name, index=False)

print(f"Result data has been written to '{file_name}'")
