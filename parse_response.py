from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

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
    openInterest: float
    bid: float
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
    openInterest: float
    bid: float
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