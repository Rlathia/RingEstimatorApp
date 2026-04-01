import requests
import configparser

# Load the config file using the Config Parser module
config = configparser.ConfigParser()
config.read("config.cfg")   

class GoldAPIService:
    def __init__(self):
        self.api_key =  config["API"]["goldapi_key"]
        self.base_url = "https://www.goldapi.io/api"

    def get_gold_price(self):
        symbol = "XAU"
        curr = "CAD"

        url = f"{self.base_url}/{symbol}/{curr}"
        
        headers = {
            "x-access-token": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            result = response.text
            return result
        except requests.exceptions.RequestException as e:
            print("Error:", str(e))
            return None

    #make_gapi_request()