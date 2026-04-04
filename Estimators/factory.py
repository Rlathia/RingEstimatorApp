from Estimators.gold_estimator import GoldCostEstimator
from Estimators.diamond_estimator import DiamondCostEstimator

class CostEstimatorFactory:

    @staticmethod
    def create_gold_estimator():
        return GoldCostEstimator()

    @staticmethod
    def create_diamond_estimator(strategy):
        return DiamondCostEstimator(strategy)