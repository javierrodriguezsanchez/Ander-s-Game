from reigns import *
from Human_Player import *
from Game import *

print("Welcome to Anders Game")
print("Select the number of players:")
Num = int(input())

Players = []
Kingdoms = []

for i in range(Num):
    Realm = Kingdom(5, 3, 3)
    Kingdoms.append(Realm)
    Players.append(Human_Player(i))

game = Game(Kingdoms, Players)
game.Run_Game()