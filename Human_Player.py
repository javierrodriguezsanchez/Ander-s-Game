from reigns import *

class Human_Player:

    def __init__(self, Index:int):
        self.index = Index

    def Play(self, Kingdoms: list):
        Moves = []
        while True:
            for j, i in enumerate(Kingdoms):
                print(f"Kingdom {j} Status:")
                print("-------------------")
                print(f"Population LV: {i.population}")
                print(f"Wall LV: {i.walls}")
                print(f"Army: {i.army}")
                print()
            
            print(f"Kingdom {self.index} Turn")
            print(f"Choose your move (Actions left {Kingdoms[self.index].available_moves})")

            Options = list(Kingdoms[self.index].actions(Kingdoms, self.index))
            for i, option in enumerate(Options):
                print(f"[{i}]  {option}")
            
            Move = int(input())
            MoveText = Options[Move][0]
            MoveValues = Options[Move][1]

            Moves.append(Options[Move])

            if(MoveText == "Pass"):
                break

            Kingdoms[self.index].act(Kingdoms, MoveText, MoveValues)
        return Moves