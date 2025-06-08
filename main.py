from api_provider import api_provider 
import time
import parse_response as parser
from datetime import datetime
import pandas as pd
from compute_volatility import solve_for_iv
import json

def main():
    ticker = 'AAPL'
    api = api_provider()
    response = api.get_expiry_dates(ticker)
    for i in response:
        print(i)
    
    current_timestamp = int(time.time())
    seconds_in_year = 31536000

    calls = {}
    puts = {}

    current_price = api.get_current_stock_price(ticker)
    history = api.request_stock_history(ticker)
    with open("file.txt", "w") as f:
        json.dump(history, f, indent=4)

    print(float(current_price))

    for i in response:
        if i < current_timestamp:
            continue
        response = api.get_options_for_ticker(ticker, i)
        processed_response = parser.process_stock_data(response)

        for call in processed_response.body[0].options[0].calls:
            datetimestamp = int(call.expiration)
            new_date_time = datetimestamp - current_timestamp
            new_date_time = new_date_time/seconds_in_year
            calls[call.contractSymbol] = (call.strike, call.ask, new_date_time)

        for put in processed_response.body[0].options[0].puts:
            datetimestamp = int(call.expiration)
            new_date_time = datetimestamp - current_timestamp
            new_date_time = new_date_time/seconds_in_year
            puts[put.contractSymbol] = (put.strike, put.ask, new_date_time)

    calls_df = pd.DataFrame.from_dict(calls, orient='index', columns=['Strike Price', 'Last Price', 'Time till expiry'])
    puts_df = pd.DataFrame.from_dict(puts, orient='index', columns=['Strike Price','Last Price', 'Time till expiry'])

    calls_df = calls_df.reset_index().rename(columns={'index': 'Contract Symbol'})
    puts_df = puts_df.reset_index().rename(columns={'index': 'Contract Symbol'})

    calls_df['Option Type'] = 'Call'
    calls_df['Price Per Unit'] = calls_df['Last Price'] + calls_df['Strike Price']
    calls_df['Current Price'] = current_price
    puts_df['Option Type'] = 'Put'
    puts_df['Price Per Unit'] = puts_df['Last Price'] + puts_df['Strike Price']
    puts_df['Current Price'] = current_price

    print()
    print(calls_df)


    # What is required. S = price of underlying (i.e. current price), 
    # K = strike price, 
    # r = risk free rate, 
    # T = time till expiry, 
    # price = current price of the option

    # ivs = []
    # x = 0

    # for i, row in calls_df.iterrows():

    #     S = float(row['Current Price'])
    #     K = float(row['Strike Price'])
    #     r = 0.075
    #     T = row['Time till expiry']
    #     price = row['Last Price']
        
    #     iv = solve_for_iv(
    #         S, K, T, r, price,
    #         sigma_guess=0.5, q=0,
    #         otype="call", N_iter=20,
    #         epsilon=0.001, verbose=True
    #     )
    #     ivs.append(iv)
    
    # calls_df['Implied Volatility'] = ivs
    # print(calls_df)

    #     x = x + 1

    # calls_df['Implied Volatility'] = ivs
    # print(calls_df.head)
    # calls_df.to_csv("calls_data.csv", index=False)



if __name__ == "__main__":
    main()