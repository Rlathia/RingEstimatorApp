from Estimators.factory import CostEstimatorFactory

class RingEstimate:

    def __init__(self, ring_size, diamond_size, diamond_count, diamond_quality):
        self.ring_size = ring_size
        self.diamond_size = diamond_size
        self.diamond_count = diamond_count
        self.diamond_quality = diamond_quality
        self.gold_estimator = CostEstimatorFactory.create_gold_estimator()
      #  self.diamond_estimator = CostEstimatorFactory.create_diamond_estimator(strategy=None)  # Replace with actual strategy

    def calculate_cost(self):
        gold_cost = self.gold_estimator.calculate_cost(self.ring_size)
        # diamond_cost = self.diamond_estimator.calculate_cost(self.diamond_size, self.diamond_count, self.diamond_quality)
        return gold_cost 
    #+ diamond_cost