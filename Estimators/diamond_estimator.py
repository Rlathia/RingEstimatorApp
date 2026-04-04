class DiamondCostEstimator:

    def __init__(self, strategy):
        self.strategy = strategy

    def calculate_cost(self, diamond_size, count, diam_quality):
        return self.strategy.calculate_price(diamond_size, count, diam_quality)