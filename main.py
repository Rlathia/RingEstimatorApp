from API.goldapi import GoldAPIService
from database import RedisClient

def main():
    gold_api_service = GoldAPIService()
    redis_client = RedisClient()
    gold_price = gold_api_service.get_gold_price("price_gram_18k")

    
    if gold_price is not None:
        print(gold_price)
        redis_client.r.set("gold_price", gold_price)
    else:
        print("Failed to retrieve gold price.")

if __name__ == "__main__":
    main()