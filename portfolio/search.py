import yfinance as yf

#This function uses yfinance to find the ticker symbol that is inputted.

def searchforstock(input):
    tickers = [f'{input}']
    for ticker in tickers:
        ticker_yahoo = yf.Ticker(ticker)
        data = ticker_yahoo.history()
        try:
            final_output = round(float((data.tail(1)['Close'].iloc[0])), 2)
            return final_output
            break
        except:
            return 'We dont have that stock on our system, please try again'
