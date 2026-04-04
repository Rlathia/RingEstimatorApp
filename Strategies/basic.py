from Strategies.pricing_strategy import PricingStrategy

class BasicPricingStrategy(PricingStrategy):
    # Strategy Pattern: Basic Pricing Strategy
    def calculate_price(self, cost):

        # Add no markup to the cost
        return cost * 1.0 