from API.goldapi import GoldAPIService

def main():
    gold_api_service = GoldAPIService()
    gold_price = gold_api_service.get_gold_price()
    
    if gold_price is not None:
        print(gold_price)
    else:
        print("Failed to retrieve gold price.")

if __name__ == "__main__":
    main()