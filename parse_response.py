from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime
import time
import parse_response as parser
from datetime import datetime
import pandas as pd
import json


class Quote(BaseModel):
    language: str
    quoteType: str
    currency: str
    marketCap: float
    regularMarketPrice: float
    regularMarketChange: float
    regularMarketChangePercent: float
    regularMarketDayHigh: float
    regularMarketDayLow: float
    regularMarketVolume: int
    fiftyTwoWeekLow: float
    fiftyTwoWeekHigh: float
    shortName: str
    longName: str
    symbol: str

class Call(BaseModel):
    contractSymbol: str
    strike: int
    currency: str
    lastPrice: float
    change: float
    percentChange: float
    volume: float
    openInterest: Optional[float]
    bid: Optional[float]
    ask: float
    contractSize: str
    expiration: float
    lastTradeDate: float
    impliedVolatility: float
    inTheMoney: bool
    volume: Optional[int] = 0

class Put(BaseModel):
    contractSymbol: str
    strike: int
    currency: str
    lastPrice: float
    change: float
    percentChange: float
    volume: float
    openInterest: Optional[float]
    bid: Optional[float]
    ask: float
    contractSize: str
    expiration: float
    lastTradeDate: float
    impliedVolatility: float
    inTheMoney: bool
    volume: Optional[int] = 0
        
class Options(BaseModel):
    expirationDate: int
    hasMiniOptions: bool
    calls: List[Call] = []
    puts: List[Put] = []

class Body(BaseModel):
    underlyingSymbol: str
    expirationDates: List[int]
    strikes: List[Any] = []
    hasMiniOptions: bool
    quote: Quote
    options: List[Options]

class Meta(BaseModel):
    ticker: str
    expiration: Optional[str] = ""
    processedTime: str
    version: str
    status: int
    copywrite: str

class StockResponse(BaseModel):
    meta: Meta
    body: List[Body]

def process_stock_data(json_data: dict) -> StockResponse:
    stock_data = StockResponse(**json_data)
    return stock_data

# def create_dataframes():
#     current_timestamp = int(time.time())
#     seconds_in_year = 31536000

#     api = api_provider()
#     calls = {}
#     puts = {}

#     current_price = api.get_current_stock_price("AMD")
#     response = api.get_expiry_dates("AMD")

#     processed_response = parser.process_stock_data(response)

#     print(float(current_price))

#     for call in processed_response.body[0].options[0].calls:
#         datetimestamp = int(call.expiration)
#         new_date_time = datetimestamp - current_timestamp
#         new_date_time = new_date_time/seconds_in_year
#         calls[call.strike] = (call.lastPrice, new_date_time)

#     for put in processed_response.body[0].options[0].puts:
#         datetimestamp = int(call.expiration)
#         new_date_time = datetimestamp - current_timestamp
#         new_date_time = new_date_time/seconds_in_year
#         puts[put.strike] = (put.lastPrice, new_date_time)

#     calls_df = pd.DataFrame.from_dict(calls, orient='index', columns=['Last Price', 'Time till expiry'])
#     puts_df = pd.DataFrame.from_dict(puts, orient='index', columns=['Last Price', 'Time till expiry'])

#     calls_df = calls_df.reset_index().rename(columns={'index': 'Strike Price'})
#     puts_df = puts_df.reset_index().rename(columns={'index': 'Strike Price'})

#     calls_df['Option Type'] = 'Call'
#     calls_df['Price Per Unit'] = calls_df['Last Price'] + calls_df['Strike Price']
#     calls_df['Current Price'] = current_price
#     puts_df['Option Type'] = 'Put'
#     puts_df['Price Per Unit'] = puts_df['Last Price'] + puts_df['Strike Price']
#     puts_df['Current Price'] = current_price

#     print()
#     print(calls_df)
