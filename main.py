from API.goldapi import GoldAPIService
from database import RedisClient
from models.ring_estimate import RingEstimate
from Strategies.basic import BasicPricingStrategy
from Strategies.premium import PremiumPricingStrategy
from Strategies.conservative import ConservativePricingStrategy

# Function to get the appropriate pricing strategy based on user choice
def get_strategy(choice):
    if choice.lower() == "basic":
        return BasicPricingStrategy()
    elif choice.lower() == "premium":
        return PremiumPricingStrategy()
    else:
        return ConservativePricingStrategy()

# Main function to run the application
def main():
    gold_api_service = GoldAPIService()
    redis_client = RedisClient()
    # Fetch the gold price from the API
    gold_price = gold_api_service.get_gold_price("price_gram_18k")

    # Store the gold price in Redis if it's successfully retrieved
    if gold_price is not None:
        print(gold_price)
        redis_client.r.set("gold_price", gold_price)
    else:
        print("Failed to retrieve gold price.")

    # Get user input for ring specifications and pricing strategy
    ring_size = int(input("Enter ring size (5, 6, or 7): "))
    diamond_size = float(input("Enter diamond size (1, 2 or 3): "))
    diamond_count = int(input("Enter number of diamonds you want in your ring: "))
    diamond_quality = input("Enter diamond quality (SI, VS, VVS): ")
    strategy_choice = input("Choose strategy (basic/premium/conservative): ")

    strategy = get_strategy(strategy_choice)
    ring_estimate = RingEstimate(ring_size, diamond_size, diamond_count, diamond_quality.lower())
    total_cost = ring_estimate.calculate_cost(strategy)

    # Print the total cost
    print(f"Total cost: {total_cost}")

     # Save to Redis
    redis_client.r.set("Estimate", total_cost)

if __name__ == "__main__":
    main()