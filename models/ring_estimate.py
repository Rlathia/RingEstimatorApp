from Estimators.factory import CostEstimatorFactory
from Memento.memento import RingMemento

class RingEstimate:

    def __init__(self, ring_size, diamond_size, diamond_count, diamond_quality, gold_price):
        self.ring_size = ring_size
        self.diamond_size = diamond_size
        self.diamond_count = diamond_count
        self.diamond_quality = diamond_quality
        self.total_cost = 0.00
        self.gold_price = gold_price

    def calculate_cost(self, strategy):

    # Factory Pattern:
        # Creates estimator objects without exposing creation logic
        self.gold_estimator = CostEstimatorFactory.create_gold_estimator()
        self.diamond_estimator = CostEstimatorFactory.create_diamond_estimator(strategy)  # Replace with actual strategy
        
        # Calculate gold and diamond costs using the respective estimators
        gold_cost = float(self.gold_estimator.calculate_gold_cost(self.ring_size, self.gold_price))
        diamond_cost = float(self.diamond_estimator.calculate_diamond_cost(self.diamond_size, self.diamond_count, self.diamond_quality))
        self.total_cost = float(gold_cost) + float(diamond_cost)
        return self.total_cost, gold_cost, diamond_cost

    # Memento Pattern:
    # Captures and restores the state of the ring estimate  
    def create_memento(self):
        return RingMemento(self.__dict__.copy())

