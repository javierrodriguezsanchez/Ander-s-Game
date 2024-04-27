from src.Strategies.Strategy import Strategy
from src.Strategies.Implementations.utils.utils import Bad_Ending_for_i, Strongest_Army, Weakest_Army
import random


class AttackWeakStrategy(Strategy):
    '''
    Attacks the kingdom with the weakest army.

    Offer/Accept alliance only with the kingdom of the strongest army.
    '''
    def __init__(self):
        pass

    def Select(self, context: dict) -> int:
        my_index = context['index']
        posible_actions = context['endings']
        
        current_state=posible_actions[0]
        less_troops = Weakest_Army(current_state, my_index)
        best_ending = Bad_Ending_for_i(posible_actions, less_troops, my_index)
        return best_ending

    def ChooseAllies(self, context: dict) -> list[bool]:
        my_index = context['index']
        Kingdoms = context['state']
        Allies = context['allies']
        
        more_troops = Strongest_Army(Kingdoms, my_index)

        prop = [False] * len(Kingdoms)
        if Allies[more_troops] > 0:
            return prop

        rand = random.random()
        if rand < 0.5:
            prop[more_troops] = True

        return prop

    def AcceptAlliance(self, context: dict) -> bool:
        my_index = context['index']
        Kingdoms = context['state']
        prop_index = context['reign']
        
        more_troops = Strongest_Army(Kingdoms ,my_index)

        if prop_index == more_troops:
            return True

        else:
            return False