from Strategies import Strategy
from reigns import Kingdom
from random import random

class Agent:
    def __init__(self,strategy:Strategy):
        self.strategy=strategy
        
    def Play(self, Kingdoms: list[Kingdom], Index):
        possible_endings, actions=self.possible_endings(Kingdoms,Index)
        selection=self.strategy.Select(possible_endings)
        moves=self.moves(actions,selection)
        return moves

    def possible_endings(self,Kingdoms: list[Kingdom], Index):
        visited_nodes=set()
        visited_nodes.add(self.GetHash(Kingdoms))
        possible_endings=[self.Copy(Kingdoms)]
        actions=[(0,("Pass",(Index,)))]
        i=0
        while i < len(possible_endings):
            for action,values in possible_endings[i].actions(possible_endings[i],Index):
                if action=='Pass':
                    continue
                copy=self.Copy(possible_endings[i])
                copy[Index].act(copy,action,values)
                hash_copy=self.GetHash(Kingdoms)
                if hash_copy in visited_nodes:
                    continue
                visited_nodes.add(hash_copy)
                possible_endings.append(copy)
                actions.append((i,(actions,values)))
        return (possible_endings,actions)

    def moves(self, actions:list[tuple[int,tuple]], selection:int)->list[tuple]:
        if selection==0:
            return [actions[0][1]]
        moves=self.moves(actions,actions[selection][0])
        aux=moves[-1]
        moves[-1]=actions[selection][1]
        moves.append(aux)
        return moves

    def GetHash(self, Kingdoms:list[Kingdom])->str:
        hashes=[x.hash() for x in  Kingdoms]
        returnValue=""
        for h in hashes:
            returnValue+=h+'\n'
        return returnValue
    def Copy(self, Kingdoms:list[Kingdom])->list[Kingdom]:
        return [Kingdom(x) for x in Kingdoms]