from src.Strategies.Strategy import Strategy
import random

class RandomStrategy(Strategy):
    '''
    Plays Random.
    '''
    def __init__(self,seed=None):
        random.seed(seed)
        
    def Select(self, context: dict) -> int:
        posible_actions = context['endings']
        
        Total = len(posible_actions)
        best_end = random.randint(0, Total - 1)
        return best_end
    
    def ChooseAllies(self, context: dict) -> list[bool]:
        my_index = context['index']
        Kingdoms = context['state']
        
        prop = [False] * len(Kingdoms)

        for i in range(len(prop)):
            if i == my_index:
                continue

            rand = random.random()
            if rand < 0.5:
                prop[i] = True

        return prop
    
    def AcceptAlliance(self, context: dict) -> bool:
        rand = random.random()
        if rand < 0.5:
            return True
        else:
            return False