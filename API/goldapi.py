import requests
import configparser

# Load the config file using the Config Parser module
config = configparser.ConfigParser()
config.read("config.cfg")   

# This class is responsible for interacting with the Gold API to fetch gold prices based on the specified parameters.
class GoldAPIService:
    def __init__(self):
        self.api_key =  config["API"]["goldapi_key"]
        self.base_url = "https://www.goldapi.io/api"

    def get_gold_price(self, price_gram):
        symbol = "XAU"
        curr = "CAD"
        price_gram = price_gram
        # Construct the URL for the API request using the base URL, symbol, and currency
        url = f"{self.base_url}/{symbol}/{curr}"
        # Set up the headers for the API request, including the API key for authentication
        headers = {
            "x-access-token": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            # Make the API request to fetch the gold price
            response = requests.get(url, headers=headers)
            # Check if the request was successful
            response.raise_for_status()

            result = response.json()
            return result[price_gram]
        
        except requests.exceptions.RequestException as e:
            print("Error:", str(e))
            return None

