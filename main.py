from API.goldapi import GoldAPIService
from Database.database import RedisClient
from Domain.ring_estimate import RingEstimate
from Strategies.basic import BasicPricingStrategy
from Strategies.premium import PremiumPricingStrategy
from Strategies.conservative import ConservativePricingStrategy
from Memento.history import History

# Function to get the appropriate pricing strategy based on user choice
def get_strategy(choice):
    if choice == "basic":
        return BasicPricingStrategy()
    elif choice == "premium":
        return PremiumPricingStrategy()
    else:
        return ConservativePricingStrategy()

# Function to display estimates from memento history
def display_estimates(history):
    message = ""
    if not history.get_history():
        message += "No estimates found. Please create an estimate first."
    else:
        for i, memento in enumerate(history.get_history()):
            state = memento.get_state()
            message += f"\nEstimate ID {i + 1}:"
            message += f"\n  Ring Size: {state['ring_size']}"
            message += f"\n  Diamond Size: {state['diamond_size']}"
            message += f"\n  Diamond Count: {state['diamond_count']}"
            message += f"\n  Diamond Quality: {state['diamond_quality']}"
            message += f"\n  Total Cost: ${state['total_cost']}\n"

    return message

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
          "\nYou can choose from different pricing strategies to see how they affect the final cost.",
          "\nYou can also save your estimates to a Redis database for future reference.")
    print("\n Let's get started!")
    
    user_name = input("\n Enter your name :")

    while True:
        print("\n===== RingCostr Menu =====")
        print("1. Create New Estimate")
        print("2. View Recently Created Estimates")
        print("3. Save Estimate")
        print("4. View Saved Estimate(s)")
        print("5. Exit")

        choice = input("Enter choice (1, 2, 3 or 4): ")

        if choice == "1":
            # Get user input for ring specifications and pricing strategy
            ring_size = int(input("Enter ring size (5, 6, or 7): "))
            diamond_size = int(input("Enter diamond size (1, 2 or 3): "))
            diamond_count = int(input("Enter number of diamonds you want in your ring: "))
            diamond_quality = input("Enter diamond quality (SI, VS or VVS): ")
            strategy_choice = input("Choose strategy (basic, conservative or premium): ")

            strategy = get_strategy(strategy_choice.lower())
            ring_estimate = RingEstimate(ring_size, diamond_size, diamond_count, diamond_quality.lower(), gold_price)
        
            # Strategy Pattern:
            # Applies selected pricing strategy to final diamond cost
            total_cost = ring_estimate.calculate_cost(strategy)

            # Print estimated cost
            print("======= Cost Breakdown =======")
            print(f"Gold cost: ${total_cost[1]: .2f}, Diamond cost: ${total_cost[2]: .2f}")
            print(f"Total Estimated Cost: ${total_cost[0]: .2f}")
            print("==============================")

            # Memento Pattern:
            # Saves the current state of the ring estimate
            memento = ring_estimate.create_memento()
            history.save(memento)

        # Display estimates from history
        elif choice == "2":
            print(f"\n===== Recently Created Estimates =====")
            print(display_estimates(history))

        # Save selected estimate to Redis
        elif choice == "3":
            # Check if there are any estimates in history before attempting to save
            if not history.get_history():
                print("No estimates to save. Please create an estimate first.")
                continue

            # Display estimates to the user and prompt for selection
            display_estimates(history)
            index = int(input("From the above displayed estimates,"
                              " enter the estimate ID to save to database: ")) - 1

            if index < 0 or index >= len(history.get_history()):
                print("Invalid estimate number. Please try again.")
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
            redis_client.save_estimate(f"{user_name}'s Estimate:{index+1}", {
            "ring_size": ring_size,
            "gold_price_CAD": round(gold_price, 2),
            "diamond_size": diamond_size,
            "diamond_count": diamond_count,
            "diamond_quality": diamond_quality,
            "total_cost_CAD": round(total_cost, 2),
           })

            print(f"Estimate {index+1} saved to Redis successfully.")

        elif choice == "4":
            print(f"\n===== {user_name}'s Saved Estimates =====")

            print("Fetching estimates...")
            user_estimates = redis_client.get_user_estimates(user_name) 
            if not user_estimates:
                print("No estimates found in Redis for this user.")
            else:
                for i, estimate in enumerate(user_estimates):
                    print(f"\nEstimate ID {i + 1}:")
                    print(f"  Ring Size: {estimate['ring_size']}")
                    print(f"  Gold Price: ${estimate['gold_price_CAD']}")
                    print(f"  Diamond Size: {estimate['diamond_size']}")
                    print(f"  Diamond Count: {estimate['diamond_count']}")
                    print(f"  Diamond Quality: {estimate['diamond_quality']}")
                    print(f"  Total Cost: ${estimate['total_cost_CAD']}")

        elif choice == "5":
            print("Thank you for using RingCostr. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()