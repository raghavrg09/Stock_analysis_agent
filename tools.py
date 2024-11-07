import yfinance as yf
import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv("gapi.env")

# Define your OpenAI client configuration
openai_api_key = os.getenv('OPENAI_KEY')
client = OpenAI(
    api_key=openai_api_key,
)


def tool_get_stock_tickers(user_query:str):
    """This function will output stock tickers as list corresponding to the user query
    Args:
        user_query: User requested query containing name of the stocks"""
    
    prompt_template = f"""Extract the list of stocks present in the provided statement as a list.
    If nothing is present, return []
    Statement:
    {user_query}
    Only return the respective stock tickers as as strings enclosed in list in the output and nothing else
    Output list:
    """
    chat_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt_template},
        ],
        temperature=0.0,
    )

    # Extract and return the response content
    output = chat_response.choices[0].message.content
    try:
        tickers = eval(output)
        return tickers
    except Exception as e:
        return f"Error in fetching the stock tickers: {e}"
    

def tool_fetch_and_save_stock_data_for_tickers(tickers_list:list):
    """This tool will input list of tickers and will fetch the stock prices and save them in a csv file with their respective tickers
    Args:
        tickers_list: list of tickers for which data needs to be fetched and saved
    """
    
    def fetch_stock_data(symbol, period = '3mo'):
        stock = yf.Ticker(symbol)
        data = stock.history(period = period)
        if not data.empty:
            data.to_csv(f"{symbol}.csv")
        else:
            raise Exception("Not able to fetch data")
    
    success = []
    fail = []
    for symbol in tickers_list:
        try:
            fetch_stock_data(symbol)
            success.append(symbol)
        except:
            fail.append(symbol)
    return f"Data successfully saved for 3 months period for {success}. Not able to fetch and save data for {fail} stocks"



def tool_calculate_stock_returns_over_a_period(ticker,n_days):
    """This function will return stock returns/average returns as percentage over a given number of days.
    Args:
        ticker: Ticker symbol of stock for which the data has to be calculated
        n_days: Number of days for which the return has to be calculated. It cannot exceed 90 days"""
    try:
        local_data = pd.read_csv(f"{ticker}.csv")
    except:
        try:
            tool_fetch_and_save_stock_data_for_tickers(tickers_list=[ticker])
            local_data = pd.read_csv(f"{ticker}.csv")
        except:
            return f"There is an error in fetching data for {ticker} stock, please try changing the stock name/ticker"
        
    if n_days:
        try:
            local_data = local_data[-n_days:]
        except Exception as e:
            print(f"Can't calculate data for {n_days} when the total data is for 3 months.\nFull error: {e}")
    # Calculate % change in returns for the past n_days
    returns = local_data['Close'].pct_change().dropna() 
    # Total return for the past n_days
    total_returns = float(returns.sum()*100)
    return f"Total returns for {ticker} stock over {n_days} days is {total_returns}%"

