from Simulation_Model.Reigns import Kingdom
from src.Strategies.Strategy import Strategy
from src.Strategies.Implementations.utils.utils import Media
import random


class AttackWeakStrategy(Strategy):
    def __init__(self):
        pass

    def Select(
        self,
        my_index: int,
        posible_actions: list[list[Kingdom]],
        reels: list[int],
        Allies: list[int],
    ) -> int:
        less_troops = -1
        troops = -1
        troop_media = -1
        current_state=posible_actions[0]
        for i in range(len(current_state)):
            if i == my_index:
                continue

            current_troops = current_state[i].army
            if len(current_troops) < troops or troops == -1:
                troops = len(current_troops)
                less_troops = i
                troop_media = Media(current_troops)

            elif len(current_troops) == troops:
                media = Media(current_troops)

                if media < troop_media:
                    troop_media = media
                    less_troops = i

        best_end = -1
        min_wall = current_state[less_troops].walls
        min_media = Media(current_state[less_troops].army)
        min_len = len(current_state[less_troops].army)
        min_pop = current_state[less_troops].population

        for i, state in enumerate(posible_actions):
            current_army = state[less_troops].army
            current_len = len(current_army)
            current_media = Media(current_army)
            current_wall = state[less_troops].walls
            current_pop = state[less_troops].population

            if current_len < min_len:
                min_len = current_len
                min_media = current_media
                min_wall = current_wall
                min_pop = current_pop
                best_end = i

            elif current_len == min_len:
                if current_media < min_media:
                    min_media = current_media
                    min_wall = current_wall
                    min_pop = current_pop
                    best_end = i

            if current_len == 0 and min_len == 0:
                if current_wall < min_wall:
                    min_wall = current_wall
                    min_pop = current_pop
                    best_end = i

                elif current_wall == min_wall:
                    if current_pop <= min_pop:
                        min_pop = current_pop
                        best_end = i

        return best_end

    def ChooseAllies(
        self,
        Kingdoms: list[Kingdom],
        my_index: int,
        reels: list[int],
        Allies: list[int],
    ) -> list[bool]:
        more_troops = -1
        troops = -1
        troop_media = -1

        for i in range(len(Kingdoms)):
            if i == my_index:
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
        more_troops = -1
        troops = -1
        troop_media = -1

        for i in range(len(Kingdoms)):
            if i == my_index:
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

        if prop_index == more_troops:
            return True

        else:
            return False