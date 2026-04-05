class DiamondCostEstimator:

    def __init__(self, strategy):
        self.strategy = strategy

    def calculate_diamond_cost(self, diamond_size, diamond_count, diamond_quality):
        cost = 0

        if diamond_size and diamond_count and diamond_quality:
            cost += (diamond_count * self.get_diamond_price(diamond_size, diamond_quality))
        
        # Strategy Pattern applied here
        return self.strategy.calculate_price(cost)
    
    #logic to retrieve diamond price based on size and quality
    def get_diamond_price(self, size, quality):
        
        # base price for Diamond
        base_price = 500.00

        size_multipliers = {
            1: 1.0,
            2: 1.5,
            3: 2.0
        }

        quality_multipliers = {
            "si": 1.0,
            "vs": 1.5,
            "vvs": 2.0
        }
    
        size_factor = size_multipliers.get(size, 1.0)
        quality_factor = quality_multipliers.get(quality, 1.0)

        cost = float(base_price * size_factor * quality_factor)

        return cost
