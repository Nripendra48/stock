import pandas as pd

# Load the Excel file
df = pd.read_excel('investment_result_2024-12-05.xlsx')

# Display the content
print(df)

# import yfinance as yf

# # Example list of Indian stock tickers
# indian_stocks = [
#     "TATAMOTORS.NS",  # Reliance Industries
#     "TCS.NS",       # Tata Consultancy Services
#     "INFY.NS",      # Infosys
#     "HDFCBANK.NS",  # HDFC Bank
#     "ICICIBANK.NS"  # ICICI Bank
# ]

# # Fetching data for each stock
# for stock in indian_stocks:
#     data = yf.download(stock, period="1d", interval="1d")
#     print(f"Data for {stock}:\n", data.tail(1))  # Printing last day's data