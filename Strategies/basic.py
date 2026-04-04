from Strategies.pricing_strategy import PricingStrategy

class BasicPricingStrategy(PricingStrategy):

    def __init__(self):
            super().__init__()

    def calculate_price(self, cost):
        # Add a 0% markup to the cost
        return cost * 1.0 