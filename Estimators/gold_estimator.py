from Database.database import RedisClient

class GoldCostEstimator:

    def __init__(self):
        pass

    def calculate_gold_cost(self, ring_size):
        # Placeholder for gold cost estimation logic
        if(ring_size == 5):
            weight = 2.2 # Example weight in grams for a ring of size 5 and band width 2mm
        elif(ring_size == 6):
            weight = 2.5 # Example weight in grams for a ring of size 7 and band width 2mm
        elif(ring_size == 7):
            weight = 2.8 # Example weight in grams for a ring of size 7 and band width 2mm
        
        redis_client = RedisClient()
        gold_price = redis_client.r.get("gold_price")

        return format((weight * float(gold_price)), '.2f' ) if gold_price else 0