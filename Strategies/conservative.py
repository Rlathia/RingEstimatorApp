from Strategies.pricing_strategy import PricingStrategy

class ConservativePricingStrategy(PricingStrategy):

    def __init__(self):
            super().__init__()

    def calculate_price(self, cost):
        # Add a 20% markup to the cost
        return cost * 1.2 
    