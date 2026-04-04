from API.goldapi import GoldAPIService
from database import RedisClient
from models.ring_estimate import RingEstimate

def main():
    gold_api_service = GoldAPIService()
    redis_client = RedisClient()
    gold_price = gold_api_service.get_gold_price("price_gram_18k")

    
    if gold_price is not None:
        print(gold_price)
        redis_client.r.set("gold_price", gold_price)
    else:
        print("Failed to retrieve gold price.")

    ring_size = int(input("Enter ring size (5, 6, or 7): "))
    ring_estimate = RingEstimate(ring_size, diamond_size=None, diamond_count=None, diamond_quality=None)
    total_cost = ring_estimate.calculate_cost()
    print(f"Total cost: {total_cost}")
    
if __name__ == "__main__":
    main()