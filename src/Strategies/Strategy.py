from src.Simulation_Model.Reigns import Kingdom


class Strategy:
    def __init__(self):
        pass

    def Select(
        self,
        my_index: int,
        posible_actions: list[list[Kingdom]],
        reels: list[int] = [],
        Allies: list[int] = [],
    ) -> int:
        pass

    def ChooseAllies(
        self,
        Kingdoms: list[Kingdom],
        my_index: int,
        reels: list[int],
        Allies: list[int],
    ) -> list[bool]:
        return [False] * len(Kingdoms)

    def AcceptAlliance(
        self,
        Kingdoms: list[Kingdom],
        my_index: int,
        prop_index: int,
        reels: list[int],
        Allies: list[int],
    ) -> bool:
        return False
