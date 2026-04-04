from Estimators.factory import CostEstimatorFactory

class RingEstimate:

    def __init__(self, ring_size, diamond_size, diamond_count, diamond_quality):
        self.ring_size = ring_size
        self.diamond_size = diamond_size
        self.diamond_count = diamond_count
        self.diamond_quality = diamond_quality
        self.total_cost = 0.00

    def calculate_cost(self, strategy):
        self.gold_estimator = CostEstimatorFactory.create_gold_estimator()
        self.diamond_estimator = CostEstimatorFactory.create_diamond_estimator(strategy)  # Replace with actual strategy
        
        # Calculate gold and diamond costs using the respective estimators
        gold_cost = self.gold_estimator.calculate_gold_cost(self.ring_size)
        diamond_cost = self.diamond_estimator.calculate_diamond_cost(self.diamond_size, self.diamond_count, self.diamond_quality)
        print(f"Gold cost: {gold_cost}, Diamond cost: {diamond_cost}")
        self.total_cost = float(gold_cost) + float(diamond_cost)
        return self.total_cost