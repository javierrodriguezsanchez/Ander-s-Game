from Simulation_Model.Reigns import Kingdom
from src.Strategies.Strategy import Strategy
from src.Strategies.Implementations.utils.utils import Media, Bad_Ending_for_i, Strongest_Army, Weakest_Army
import random


class AttackWeakStrategy(Strategy):
    '''
    Attacks the kingdom with the weakest army.

    Offer/Accept alliance only with the kingdom of the strongest army.
    '''
    def __init__(self):
        pass

    def Select(
        self,
        my_index: int,
        posible_actions: list[list[Kingdom]],
        reels: list[int],
        Allies: list[int],
    ) -> int:
        
        current_state=posible_actions[0]
        less_troops = Weakest_Army(current_state, my_index)
        best_ending = Bad_Ending_for_i(posible_actions, less_troops)
        return best_ending

    def ChooseAllies(
        self,
        Kingdoms: list[Kingdom],
        my_index: int,
        reels: list[int],
        Allies: list[int],
    ) -> list[bool]:
        
        more_troops = Strongest_Army(Kingdom, my_index)

        prop = [False] * len(Kingdoms)
        if Allies[more_troops] > 0:
            return prop

        rand = random.random()
        if rand < 0.5:
            prop[more_troops] = True

        return prop

    def AcceptAlliance(
        self,
        Kingdoms: list[Kingdom],
        my_index: int,
        prop_index: int,
        reels: list[int],
        Allies: list[int],
    ) -> bool:
        
        more_troops = Strongest_Army(Kingdom ,my_index)

        if prop_index == more_troops:
            return True

        else:
            return False