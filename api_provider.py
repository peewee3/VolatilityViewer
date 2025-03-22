from dotenv import load_dotenv
import os
import requests

load_dotenv()

class api_provider:
	def __init__(self):
		self.api_key = os.getenv("RAPIDAPI_KEY")
		if not self.api_key:
			raise ValueError("RAPIDAPI_KEY environment variable not set")
		
		self.headers = {
			"x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "yahoo-finance15.p.rapidapi.com"
		}

	def request_stock_history(self, ticker):
		url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/stock/history"

		querystring = {"symbol":f"{ticker}","interval":"3mo","diffandsplits":"false"}

		try:
			response = requests.get(url, headers=self.headers, params=querystring)
			response.raise_for_status() 
			return response.json()
		except requests.exceptions.RequestException as e:
			print(f"Error fetching stock history: {e}")
			return None
	
	def get_current_stock_price(self, stockName):
		url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/quote"

		querystring = {"ticker":f"{stockName}","type":"STOCKS"}

		try:
			response = requests.get(url, headers=self.headers, params=querystring)
			response.raise_for_status()
			response = response.json()
			body = response['body']
			primaryData = body['primaryData']
			price = primaryData['lastSalePrice']
			return price
		except requests.exceptions.RequestException as e:
			print(f"Error fetching current stock price: {e}")
			return None

	def print_stock_history(self, api_response):
		metaData = api_response.get("meta")
		body = api_response.get("body")

		print(len(metaData))
		print(len(body))

		for x in metaData:
			string = str(x) + ": " + str(metaData[x])
			print(string)
		
		for x in body:
			string = str(x) + ": " + str(body[x])
			print(string)

	def get_options_for_ticker(self, ticker):

		url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/options"

		querystring = {"ticker":f"{ticker}"}

		try:
			response = requests.get(url, headers=self.headers, params=querystring)
			response.raise_for_status()
			return response.json()
		except requests.exceptions.RequestException as e:
			print(f"Error fetching options for ticker: {e}")
			return None