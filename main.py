from API.goldapi import GoldAPIService
from Database.database import RedisClient
from Memento.memento import RingMemento
from Models.ring_estimate import RingEstimate
from Strategies.basic import BasicPricingStrategy
from Strategies.premium import PremiumPricingStrategy
from Strategies.conservative import ConservativePricingStrategy
from Memento.history import History

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
    history = History()
    # Fetch the gold price from the API
    gold_price = gold_api_service.get_gold_price("price_gram_18k")

    # Store the gold price in Redis if it's successfully retrieved
    if gold_price is not None:
        redis_client.r.set("gold_price", gold_price)
    else:
        print("Failed to retrieve gold price.")

    # Get user input for ring specifications and pricing strategy
    ring_size = int(input("Enter ring size (5, 6, or 7): "))
    diamond_size = int(input("Enter diamond size (1, 2 or 3): "))
    diamond_count = int(input("Enter number of diamonds you want in your ring: "))
    diamond_quality = input("Enter diamond quality (SI, VS, VVS): ")
    strategy_choice = input("Choose strategy (basic/premium/conservative): ")

    strategy = get_strategy(strategy_choice)
    ring_estimate = RingEstimate(ring_size, diamond_size, diamond_count, diamond_quality.lower())
    
# Strategy Pattern:
    # Allows switching between different diamond pricing algorithms
    # Applies selected pricing strategy to final diamond cost
    total_cost = ring_estimate.calculate_cost(strategy)

    # Print the total cost
    print(f"Total Estimated Cost: {total_cost}")

     # Save to Redis
    redis_client.r.hset("latest_estimate", mapping={
        "ring_size": ring_size,
        "gold_price": gold_price,
        "diamond_size": diamond_size,
        "diamond_count": diamond_count,
        "diamond_quality": diamond_quality,
        "strategy": strategy_choice,
        "total_cost": total_cost,
    })

    print("Estimate saved to Redis.")
    print(redis_client.r.hgetall("latest_estimate"))

# Memento Pattern:
    # Saves the current state of the ring estimate
    memento = ring_estimate.create_memento()
    print('ok', history)
    history.save(memento)

    print("State saved to history.")

if __name__ == "__main__":
    main()