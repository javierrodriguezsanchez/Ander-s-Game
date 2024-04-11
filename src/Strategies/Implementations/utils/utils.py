from src.Simulation_Model.Reigns import Kingdom
import random

def Media(colection):
    sum_ = sum(colection)
    den = len(colection)
    if den==0:
        return 0
    return int(sum_/den)

def Bad_Ending_for_i(posible_actions: list[list[Kingdom]], i: int)-> int:
    '''
    Returns the index of the worst ending for the kingdom i
    '''
    current_state=posible_actions[0]

    best_end = -1
    min_wall = current_state[i].walls
    min_media = Media(current_state[i].army)
    min_len = len(current_state[i].army)
    min_pop = current_state[i].population

    for j, state in enumerate(posible_actions):
        current_army = state[i].army
        current_len = len(current_army)
        current_media = Media(current_army)
        current_wall = state[i].walls
        current_pop = state[i].population

        if not state[i].king_alive:
            best_end = j
            break

        if current_len < min_len:
            min_len = current_len
            min_media = current_media
            min_wall = current_wall
            min_pop = current_pop
            best_end = j

        elif current_len == min_len:
            if current_media < min_media:
                min_media = current_media
                min_wall = current_wall
                min_pop = current_pop
                best_end = j

        if current_len == 0 and min_len == 0:
            if current_wall < min_wall:
                min_wall = current_wall
                min_pop = current_pop
                best_end = j

            elif current_wall == min_wall:
                if current_pop <= min_pop:
                    min_pop = current_pop
                    best_end = j

        return best_end
    
def Defensive_Ending_For_i(posible_actions: list[list[Kingdom]], i: int)-> int:
    '''
    Returns the index of the best defensive final for the kingdom i.
    '''

    initial_wall = posible_actions[0][i].walls
    greater_wall = -1
    greater_wall_state = -1
    greater_media = -1
    greater_media_state = -1
    greater_media_of_valid_states = -1
    best_ending = -1

    for j, state in enumerate(posible_actions):
        current_wall = state[i].walls
        current_army = state[i].army
        current_len = len(current_army)
        current_media = Media(current_army)
        current_min = min(current_army)

        if current_wall > greater_wall:
            greater_wall = current_wall
            greater_wall_state = j

        if current_media > greater_media:
            greater_media = current_media
            greater_media_state = j

        if current_wall - initial_wall >= 2 and current_len >= 3 and current_min >= 3:
            if current_media > greater_media_of_valid_states:
                greater_media_of_valid_states = current_media
                best_ending = j

    if best_ending != -1:
        return best_ending
    else:
        rand = random.random()
        if rand < 0.5:
            return greater_wall_state
        else:
            return greater_media_state

    
def Strongest_Army(Kingdoms: list[Kingdom], my_index: int) -> int:
    '''
    Returns the index of the kingdom with the strongest army (if my_index = -1 includes all the kingdoms in the comparison)
    '''

    more_troops = -1
    troops = -1
    troop_media = -1

    for i in range(len(Kingdoms)):
        if i == my_index or not Kingdoms[i].king_alive:
            continue

        current_troops = Kingdoms[i].army
        if len(current_troops) > troops:
            troops = len(current_troops)
            more_troops = i
            troop_media = Media(current_troops)

        elif len(current_troops) == troops:
            media = Media(current_troops)

            if media > troop_media:
                troop_media = media
                more_troops = i

    return more_troops

def Weakest_Army(Kingdoms: list[Kingdom], my_index: int) -> int:
    '''
    Return the index of the kingdom with the weakest army (if my_index = -1 includes all the kingdoms in the comparison)
    '''

    less_troops = -1
    troops = -1
    troop_media = -1
    
    for i in range(len(Kingdoms)):
        if i == my_index or not Kingdoms[i].king_alive:
            continue

        current_troops = Kingdoms[i].army
        if len(current_troops) < troops or troops == -1:
            troops = len(current_troops)
            less_troops = i
            troop_media = Media(current_troops)

        elif len(current_troops) == troops:
            media = Media(current_troops)

            if media < troop_media:
                troop_media = media
                less_troops = i

    return less_troops