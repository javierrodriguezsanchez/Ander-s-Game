from reigns import *
from Human_Player import *
import os

class Game:

    def __init__(self, Kingdoms: list, Players: list):
        self.kingdoms = Kingdoms
        self.players = Players

    def Run_Game(self):
        Current_Turn = 0
        while True:
            os.system("cls")
            self.kingdoms[Current_Turn].NewTurn()
            Moves = self.players[Current_Turn].Play(self.kingdoms)

            for i in Moves:
                if (i[0] == "Attack King"):
                    self.players.pop(i[0][2])
                    self.kingdoms.pop(i[0][2])

            Current_Turn += 1
            if (Current_Turn >= len(self.players)):
                Current_Turn = 0

            if len(self.players) == 1:
                break