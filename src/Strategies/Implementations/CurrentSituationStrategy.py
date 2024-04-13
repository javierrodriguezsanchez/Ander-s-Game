from src.Simulation_Model.Reigns import Kingdom
from src.Strategies.Strategy import Strategy
from src.Strategies.Implementations.utils.utils import Bad_Ending_for_i, Strongest_Army, Weakest_Army, Defensive_Ending_For_i, Compare_Power
import random

class CurrentSituationStrategy(Strategy):
    '''
    Makes decisions according to the level of power that he has compared to other kingdoms
    '''

    def Select(
        self,
        my_index: int,
        posible_actions: list[list[Kingdom]],
        reels: list[int],
        Allies: list[int]
    ) -> int:
        
        current_state = posible_actions[0]
        my_position = -1
        best_ending = -1

        position_table = Compare_Power(current_state)

        for i in range(len(position_table)):
            if position_table[i] == my_index:
                my_position = i
                break

        if my_position == 0:
            rand = random.random()
            if rand < 0.7:
                best_ending = Defensive_Ending_For_i(posible_actions, my_index)
            else:
                bool_ = self.Attack(position_table[1], reels, Allies)
                if bool_:
                    best_ending = Bad_Ending_for_i(posible_actions, position_table[1], my_index)
                else:
                    best_ending = Defensive_Ending_For_i(posible_actions, my_index)

        elif my_position < len(position_table) - 1:
            rand = random.random()
            first_in_table = position_table[my_position - 1]
            later_in_table = position_table[my_position + 1]

            if rand < 0.5:
                bool_ = self.Attack(first_in_table, reels, Allies)
                if bool_:
                    best_ending = Bad_Ending_for_i(posible_actions, first_in_table, my_index)
                else:
                    best_ending = Defensive_Ending_For_i(posible_actions, my_index)
            elif rand < 0.9:
                bool_ = self.Attack(later_in_table, reels, Allies)
                if bool_:
                    best_ending = Bad_Ending_for_i(posible_actions, later_in_table, my_index)
                else:
                    best_ending = Defensive_Ending_For_i(posible_actions, my_index)
            else:
                best_ending = Defensive_Ending_For_i(posible_actions, my_index)

        else:
            first_in_table = position_table[my_position - 1]
            bool_ = self.Attack(first_in_table, reels, Allies)
            if bool_:
                best_ending = Bad_Ending_for_i(posible_actions, first_in_table, my_index)
            else:
                best_ending = Defensive_Ending_For_i(posible_actions, my_index)

        return best_ending
    
    def ChooseAllies(
        self,
        Kingdoms: list[Kingdom],
        my_index: int,
        reels: list[int],
        Allies: list[int],
    ) -> list[bool]:
        
        prop = [False] * len(Kingdoms)

        position_table = Compare_Power(Kingdoms)
        
        if position_table[0] == my_index:
            for i in range(len(reels)):
                if i == my_index or not Kingdoms[i].king_alive or Allies[i] > 0:
                    continue
                
                if reels[i] >= 10:
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
        
        if reels[prop_index] <= 0:
            return False
        
        my_position = -1
        prop_position = -1

        position_table = Compare_Power(Kingdoms)

        for i in len(position_table):
            if position_table[i] == my_index:
                my_position = i

            if position_table[i] == prop_index:
                prop_position = i

        dif = abs(prop_position - my_position)

        if dif == 1:
            return False
        else:
            rand = random.random()
            if rand < 0.5:
                return True
            else:
                return False

    def Attack(self, enemy_index: int, reels: list[int], Allies: list[int]) -> bool:
        if Allies[enemy_index] > 0:
            rand = random.random()
            if rand < 0.95:
                return False
            else:
                return True
            
        elif reels[enemy_index] > 5:
            rand = random.random()
            if rand < 0.75:
                return False
            else:
                return True
            
        elif reels[enemy_index] >= 0:
            rand = random.random()
            if rand < 0.6:
                return True
            else:
                return False
            
        else:
            return True