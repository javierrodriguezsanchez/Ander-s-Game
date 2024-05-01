from src.Simulation_Model.Reigns import Kingdom
from src.Strategies.Strategy import Strategy
from src.Agent.Knowledge_Base import Knowledge_Base


class Agent:
    def __init__(self, strategy: Strategy, KB: Knowledge_Base|None = None):
        self.KB = Knowledge_Base() if KB==None else KB
        self.KB.Learn("strategy", {"strategy": strategy})
        
        strategyname = str(self.KB.strategy)

        Parts = strategyname.split('.')

        for i in range(len(Parts)):
            if Parts[i] == "Implementations":
                strategyname = Parts[i+1]
                break
        self.strategy_name = strategyname


    def Number_Of_Players(self, n):
        self.KB.Learn("number of kingdoms", {"number": n})

    def Update_State(self, Kingdoms: list[Kingdom], Index, Actions, LastPlayer):
        self.KB.Learn("current state", {"state": Kingdoms, "Index": Index})
        if Actions==None:
            return
        if LastPlayer==Index:
            return
        DeffenseAction=0
        OffensiveAction=0
        numberOfTroopsCreated=0
        Targets=[0]*len(Kingdoms)
        for i in range(len(Actions)):
            if Actions[i]["action"]=="Upgrade Walls":
                DeffenseAction+=Actions[i]["upgrade"]
            elif Actions[i]["action"]=="Create Troop":
                OffensiveAction+=Actions[i]["level"]
                numberOfTroopsCreated+=1
            elif Actions[i]["action"]=="Upgrade Troop":
                OffensiveAction+=Actions[i]["upgrade"]
            elif Actions[i]["action"]!="Pass":
                Targets[Actions[i]["target"]]+=1
        if sum(Targets)==0:
            Targets[Index]+=1
        self.KB.Learn("actions made", {
            'player':LastPlayer,
            'actions':{'defense':DeffenseAction,'attack':OffensiveAction,'targets':Targets, "troops created":numberOfTroopsCreated}
        })
            
            

    def Percept_Attack(self, attacker: int, defender: int, objetive: str):
        self.KB.Learn(
            "attack made",
            {"attacker": attacker, "defender": defender, "objetive": objetive},
        )

    def Propose_Alliance(self):
        return self.KB.Think("possible allies")

    def Accept_Alliance(self, index: int):
        return self.KB.Think("accept alliance", {"reign": index})

    def Alliance_Answer(self, index: int, answer: bool):
        return self.KB.Think("alliance answer", {"reign": index, "answer": answer})

    def Play(self):
        possible_endings = self.KB.Think("possible endings")
        selection = self.KB.Think("best ending", {"endings": possible_endings})
        moves = self.KB.Think("actions for best ending", {"selection": selection})
        return moves

    def EndTurn(self):
        self.KB.Learn("end of the turn", {})
