class PricingStrategy:

    def __init__(self):
        pass

    def calculate_price(self, cost):
        raise NotImplementedError("Subclasses must implement calculate_price()")