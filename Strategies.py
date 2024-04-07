from Agent_Player import Strategy
from reigns import Kingdom
import random

class RandomStrategy(Strategy):
    def __init__(self,seed=None):
        random.seed(seed)
    def Select(self,posible_actions:list[list[Kingdom]])->int:
        return random.choice(range(len(posible_actions)))

class MultipleStrategy(Strategy):
    def __init__(self,strategies:list[Strategy],priorities:list[int]):
        self.strategies=strategies[0:min(len(priorities),len(strategies))]
        priorities=priorities[0:min(len(priorities),len(strategies))]
        self.priorities=[sum(priorities[0:i+1])/sum(priorities) for i in range(len(priorities))]
    def Select(self,posible_actions:list[list[Kingdom]])->int:
        i=random.random()
        for p in range(len(self.priorities)):
            if i<self.priorities[p]:
                return self.strategies[p].Select(posible_actions)