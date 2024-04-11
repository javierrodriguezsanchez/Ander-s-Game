from src.Simulation_Model.Reigns import Kingdom
from src.Strategies.Strategy import Strategy
from src.Simulation_Model.Reigns import Kingdom
import random

class RandomStrategy(Strategy):
    '''
    Plays Random.
    '''
    def __init__(self,seed=None):
        random.seed(seed)
        
    def Select(
        self,
        my_index: int,
        posible_actions: list[list[Kingdom]],
        reels: list[int],
        Allies: list[int],
    ) -> int:
        
        return random.choice(range(len(posible_actions)))
    
    def ChooseAllies(
        self,
        Kingdoms: list[Kingdom],
        my_index: int,
        reels: list[int],
        Allies: list[int],
    ) -> list[bool]:
        
        prop = [False] * len(Kingdoms)

        for i in range(len(prop)):
            if i == my_index:
                continue

            rand = random.random()
            if rand < 0.5:
                prop[i] = True

        return prop
    
    def AcceptAlliance(
        self,
        Kingdoms: list[Kingdom],
        my_index: int,
        prop_index: int,
        reels: list[int],
        Allies: list[int],
    ) -> bool:
        
        rand = random.random()
        if rand < 0.5:
            return True
        else:
            return False