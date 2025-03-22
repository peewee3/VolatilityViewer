from APIProvider import api_provider 
import time
import parseResponse as parser
from datetime import datetime
import pandas as pd
from computeVolatility import compute_implied_volatility

def main():
    current_timestamp = int(time.time())
    seconds_in_year = 31536000

    api = api_provider()
    calls = {}
    puts = {}

    current_price = api.get_current_stock_price("AMD")
    response = api.get_options_for_ticker("AMD")
    processed_response = parser.process_stock_data(response)

    for call in processed_response.body[0].options[0].calls:
        datetimestamp = int(call.expiration)
        new_date_time = datetimestamp - current_timestamp
        new_date_time = new_date_time/seconds_in_year
        calls[call.strike] = (call.lastPrice, new_date_time)

    for put in processed_response.body[0].options[0].puts:
        datetimestamp = int(call.expiration)
        new_date_time = datetimestamp - current_timestamp
        new_date_time = new_date_time/seconds_in_year
        puts[put.strike] = (put.lastPrice, new_date_time)

    calls_df = pd.DataFrame.from_dict(calls, orient='index', columns=['Last Price', 'Time till expiry'])
    puts_df = pd.DataFrame.from_dict(puts, orient='index', columns=['Last Price', 'Time till expiry'])

    calls_df = calls_df.reset_index().rename(columns={'index': 'Strike Price'})
    puts_df = puts_df.reset_index().rename(columns={'index': 'Strike Price'})

    calls_df['Option Type'] = 'Call'
    calls_df['Price Per Unit'] = calls_df['Last Price'] + calls_df['Strike Price']
    calls_df['Current Price'] = current_price
    puts_df['Option Type'] = 'Put'
    puts_df['Price Per Unit'] = puts_df['Last Price'] + puts_df['Strike Price']
    puts_df['Current Price'] = current_price

    print(calls_df.head)

    compute_implied_volatility(calls_df)

if __name__ == "__main__":
    main()