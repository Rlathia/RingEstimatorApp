from API.goldapi import GoldAPIService
from Database.database import RedisClient
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
    
def display_estimates(history):
    if not history.get_history():
        print("No estimates found. Please create an estimate first.")
        return
    
    print("\n===== Saved Estimates =====")

    for i, memento in enumerate(history.get_history()):
        state = memento.get_state()
        print(f"\nEstimate ID {i + 1}:")
        print(f"  Ring Size: {state['ring_size']}")
        print(f"  Diamond Size: {state['diamond_size']}")
        print(f"  Diamond Count: {state['diamond_count']}")
        print(f"  Diamond Quality: {state['diamond_quality']}")
        print(f"  Total Cost: ${state['total_cost']}\n")

# Main function to run the application
def main():
    redis_client = RedisClient()
    history = History()
    # Fetch the gold price from the API
    gold_api_service = GoldAPIService()
    gold_price = gold_api_service.get_gold_price("price_gram_18k")

    print("Welcome to RingCostr - Your Custom Ring Cost Estimator!")
    print(f"Current Gold Price (18k per gram): ${gold_price: .2f}")
    print("===============================================")
    print("This application allows you to create custom ring estimates based on your specifications.",
          "You can choose from different pricing strategies to see how they affect the final cost.",
          "You can also save your estimates to a Redis database for future reference.")
    print("\n Let's get started!")
    
    user_name = input("\n Enter your name :")

    while True:
        print("\n===== RingCostr Menu =====")
        print("1. Create New Estimate")
        print("2. View Estimates")
        print("3. Save Estimate to Database")
        print("4. Exit")

        choice = input("Enter choice (1, 2, 3 or 4): ")

        if choice == "1":
            # Get user input for ring specifications and pricing strategy
            ring_size = int(input("Enter ring size (5, 6, or 7): "))
            diamond_size = int(input("Enter diamond size (1, 2 or 3): "))
            diamond_count = int(input("Enter number of diamonds you want in your ring: "))
            diamond_quality = input("Enter diamond quality (SI, VS, VVS): ")
            strategy_choice = input("Choose strategy (basic/premium/conservative): ")

            strategy = get_strategy(strategy_choice)
            ring_estimate = RingEstimate(ring_size, diamond_size, diamond_count, diamond_quality.lower(), gold_price)
        
            # Strategy Pattern:
            # Allows switching between different diamond pricing algorithms
            # Applies selected pricing strategy to final diamond cost
            total_cost = ring_estimate.calculate_cost(strategy)

            # Print the total cost
            print(f"Total Estimated Cost: {total_cost: .2f}")

            # Memento Pattern:
            # Saves the current state of the ring estimate
            memento = ring_estimate.create_memento()
            history.save(memento)

            print("Estimate saved (Memento created).")

        # Display estimates from history
        elif choice == "2":
            print("\n===== Estimate History =====")
            display_estimates(history)

        # Save selected estimate to Redis
        elif choice == "3":
            # Check if there are any estimates in history before attempting to save
            if not history.get_history():
                print("No estimates to save. Please create an estimate first.")
                continue

            # Display estimates to the user and prompt for selection
            display_estimates(history)
            index = int(input("From the above displayed estimates,"
                              "Enter the estimate ID to save to Redis: ")) - 1

            if index < 0 or index >= len(history.get_history()):
                print("Invalid estimate number.")
                continue   

            # Retrieve the selected estimate from history
            selected_memento = history.get_history()[index]
            state = selected_memento.get_state()
            ring_size = state['ring_size']
            diamond_size = state['diamond_size']
            diamond_count = state['diamond_count']
            diamond_quality = state['diamond_quality']
            total_cost = state['total_cost']

            # Save selected estimate to Redis
            redis_client.save_estimate(f"{user_name}'s Estimate:{index+1}", mapping={
            "ring_size": ring_size,
            "gold_price": gold_price,
            "diamond_size": diamond_size,
            "diamond_count": diamond_count,
            "diamond_quality": diamond_quality,
            "total_cost": total_cost,
           })

            print(f"Estimate {index+1} saved to Redis successfully.")

        elif choice == "4":
            print("Thank you for using RingCostr. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()