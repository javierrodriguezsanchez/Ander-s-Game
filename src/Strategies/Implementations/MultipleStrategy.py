from src.Strategies.Strategy import Strategy
from src.Simulation_Model.Reigns import Kingdom
import random

class MultipleStrategy(Strategy):
    def __init__(self,strategies:list[Strategy],priorities:list[int]):
        self.strategies=strategies[0:min(len(priorities),len(strategies))]
        priorities=priorities[0:min(len(priorities),len(strategies))]
        self.priorities=[sum(priorities[0:i+1])/sum(priorities) for i in range(len(priorities))]

    def Select(
        self,
        my_index: int,
        posible_actions: list[list[Kingdom]],
        reels: list[int] = [],
        Allies: list[int] = []
    ) -> int:
        i=random.random()
        for p in range(len(self.priorities)):
            if i<self.priorities[p]:
                return self.strategies[p].Select(my_index,posible_actions,reels,Allies)
            
    def ChooseAllies(
        self,
        Kingdoms: list[Kingdom],
        my_index: int,
        reels: list[int],
        Allies: list[int]
    ) -> list[bool]:
        i=random.random()
        for p in range(len(self.priorities)):
            if i<self.priorities[p]:
                return self.strategies[p].ChooseAllies(my_index,Kingdoms,reels,Allies)

    def AcceptAlliance(
        self,
        Kingdoms: list[Kingdom],
        my_index: int,
        prop_index: int,
        reels: list[int],
        Allies: list[int]
    ) -> bool:
        i=random.random()
        for p in range(len(self.priorities)):
            if i<self.priorities[p]:
                return self.strategies[p].ChooseAllies(Kingdoms,my_index,prop_index,reels,Allies)