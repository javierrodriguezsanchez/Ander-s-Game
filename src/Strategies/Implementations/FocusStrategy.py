from src.Simulation_Model.Reigns import Kingdom
from src.Strategies.Strategy import Strategy
from src.Strategies.Implementations.utils.utils import Bad_Ending_for_i, Strongest_Army, Weakest_Army, Defensive_Ending_For_i, Compare_Power
import random

class FocusStrategy(Strategy):
    '''
    Focus on one kingdom (according to the reels) and keep attacking him until he dies. Then Change the target.
    '''

    def __init__(self):
        self.target = -1

    def Select(
        self,
        my_index: int,
        posible_actions: list[list[Kingdom]],
        reels: list[int] = [],
        Allies: list[int] = [],
    ) -> int:
        
        current_state = posible_actions[0]

        if self.target != -1:
            if not current_state[self.target].king_alive:
                self.target = -1

        if self.target == -1:
            posible_targets = []
            No_Allies = []

            for i in range(len(reels)):
                if i == my_index or not current_state[i].king_alive:
                    continue

                if Allies[i] == 0:
                    No_Allies.append(i)
                    if reels[i] <= 0:
                        posible_targets.append(i)

            if len(posible_targets) > 0:
                self.target = random.choice(posible_targets)

            elif len(No_Allies) > 0:
                self.target = random.choice(No_Allies)

            else:
                Target = -1
                while(True):
                    Target = random.randint(0, len(current_state) - 1)

                    if Target != my_index and current_state[Target].king_alive:
                        self.target = Target
                        break

        best_end = Bad_Ending_for_i(posible_actions, self.target, my_index)
        return best_end

           
    def ChooseAllies(
        self,
        Kingdoms: list[Kingdom],
        my_index: int,
        reels: list[int],
        Allies: list[int],
    ) -> list[bool]:
        
        props = [False] * len(Kingdoms)

        for i in range(len(reels)):
            if i == my_index or Allies[i] > 0 or not Kingdoms[i].king_alive or i == self.target:
                continue

            if reels[i] >= 5:
                rand = random.random()
                if rand < 0.5:
                    props[i] = True

        return props
    
    def AcceptAlliance(
        self,
        Kingdoms: list[Kingdom],
        my_index: int,
        prop_index: int,
        reels: list[int],
        Allies: list[int],
    ) -> bool:
        
        if reels[prop_index] > 0 and prop_index != self.target:
            rand = random.random()
            if rand < 0.5:
                return True
        
        return False