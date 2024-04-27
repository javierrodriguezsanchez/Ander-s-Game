from src.Strategies.Strategy import Strategy
import random

class MultipleStrategy(Strategy):
    '''
    Receives many other strategies on the constructor with their importances.

    Returns a final choosed by one of the strategies accordin to their importances
    '''
    def __init__(self,strategies:list[Strategy],priorities:list[int]):
        self.strategies=strategies[0:min(len(priorities),len(strategies))]
        priorities=priorities[0:min(len(priorities),len(strategies))]
        self.priorities=[sum(priorities[0:i+1])/sum(priorities) for i in range(len(priorities))]

    def Select(self, context: dict) -> int:
        my_index = context['index']
        posible_actions = context['endings']
        reels = context['relations']
        Allies = context['allies']

        i=random.random()
        for p in range(len(self.priorities)):
            if i<self.priorities[p]:
                return self.strategies[p].Select(my_index,posible_actions,reels,Allies)
            
    def ChooseAllies(self, context: dict) -> list[bool]:
        my_index = context['index']
        Kingdoms = context['state']
        reels = context['relations']
        Allies = context['allies']

        i=random.random()
        for p in range(len(self.priorities)):
            if i<self.priorities[p]:
                return self.strategies[p].ChooseAllies(Kingdoms, my_index, reels, Allies)

    def AcceptAlliance(self, context: dict) -> bool:
        my_index = context['index']
        Kingdoms = context['state']
        prop_index = context['reign']
        reels = context['relations']
        Allies = context['allies']

        i=random.random()
        for p in range(len(self.priorities)):
            if i<self.priorities[p]:
                return self.strategies[p].AcceptAlliance(Kingdoms,my_index,prop_index,reels,Allies)