from src.Simulation_Model.Reigns import Kingdom

class Strategy:
    def __init__(self):
        pass
    def Select(self,posible_actions:list[list[Kingdom]],reels:list[int]=[],Allies:list[int]=[])->int:
        pass

    def ChooseAllies(self,Kingdoms:list[Kingdom],reels:list[int],Allies:list[int])->list[bool]:
        return [False]*len(Kingdoms)
    
    def AcceptAliance(self,Kingdoms:list[Kingdom],reels:list[int],Allies:list[int])->bool:
        return False