import yfinance as yf

def searchforstock(input):
    tickers = [f'{input}']
    for ticker in tickers:
        ticker_yahoo = yf.Ticker(ticker)
        data = ticker_yahoo.history()
        try:
            last_quote = (data.tail(1)['Close'].iloc[0])
            pre_output = float(last_quote)
            output = round(pre_output, 2)
            final_output = output
            return final_output
            break
        except:
            return 'We dont have that stock on our system, please try again'
