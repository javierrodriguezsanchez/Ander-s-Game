from src.Simulation_Model.Reigns import Kingdom
from src.Strategies.Strategy import Strategy
from src.Agent.Knowledge_Base import Knowledge_Base


class Agent:
    def __init__(self, strategy: Strategy, KB: Knowledge_Base|None = None):
        self.KB = Knowledge_Base() if KB==None else KB
        self.KB.Learn("strategy", {"strategy": strategy})

    def Number_Of_Players(self, n):
        self.KB.Learn("number of kingdoms", {"number": n})

    def Update_State(self, Kingdoms: list[Kingdom], Index):
        self.KB.Learn("current state", {"state": Kingdoms, "Index": Index})

    def Percept_Attack(self, attacker: int, defender: int, objetive: str):
        self.KB.Learn(
            "attack made",
            {"attacker": attacker, "defender": defender, "objetive": objetive},
        )

    def Propose_Alliance(self):
        return self.KB.Think("possible allies")

    def Accept_Alliance(self, index: int):
        return self.KB.Think("accept alliance", {"reign": index})

    def Alliance_Answer(self, index: int, answer:bool):
        return self.KB.Think("alliance answer", {"reign": index, "answer": answer})

    def Play(self):
        possible_endings = self.KB.Think("possible endings")
        selection = self.KB.Think("best ending", {"endings": possible_endings})
        moves = self.KB.Think("actions for best ending", {"selection": selection})
        return moves

    def EndTurn(self):
        self.KB.Learn("end of the turn",{})

    def clone(self):
        return Agent(self.KB.strategy, self.KB)
