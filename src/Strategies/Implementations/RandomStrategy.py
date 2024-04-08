from src.Strategies.Strategy import Strategy
from src.Simulation_Model.Reigns import Kingdom
import random

class RandomStrategy(Strategy):
    def __init__(self,seed=None):
        random.seed(seed)
        
    def Select(self,posible_actions:list[list[Kingdom]])->int:
        return random.choice(range(len(posible_actions)))