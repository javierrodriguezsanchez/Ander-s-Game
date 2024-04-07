from reigns import Kingdom

class Strategy:
    def __init__(self):
        pass
    def Select(self,posible_actions:list[list[Kingdom]])->int:
        pass

class Agent:
    def __init__(self,strategy:Strategy):
        self.KB=Knowledge_Base()
        self.KB.Tell({'type':'def strategy','strategy':strategy})
        
    def Play(self, Kingdoms: list[Kingdom], Index):
        self.KB.Tell({'type':'current state','state':Kingdoms,'Index':Index})
        possible_endings=self.KB.Ask('possible endings')
        selection=self.KB.Ask('select ending',{'endings':possible_endings})
        moves=self.KB.Ask('actions for best ending',{'selection':selection})
        return moves

class Knowledge_Base:
    def __init__(self):
        self.strategy=None
        self.current_state=None
        self.Index=None
        self.endings=None
        self.actions=None
        self.reels=None
        self.alliance=None
    
    def Tell(self,Info:dict):
        if Info['type']=='def strategy':
            self.strategy=Info['strategy']
        if Info['type']=='current state':
            self.current_state=Info['state']
            self.Index=Info['Index']
    
    def Ask(self,query:str,Info:dict=dict()):
        if query=='possible endings':
            self.possible_endings()
            return self.endings
        if query=='select ending':
            return self.strategy.Select(Info['endings'])
        if query=='actions for best ending':
            return self.moves(self.actions,Info['selection'])
            
    def possible_endings(self):
        visited_nodes=set()
        visited_nodes.add(self.GetHash(self.current_state))
        possible_endings=[self.Copy(self.current_state)]
        actions=[(0,("Pass",(self.Index,)))]
        i=0
        while i < len(possible_endings):
            for action,values in possible_endings[i].actions(possible_endings[i],self.Index):
                if action=='Pass':
                    continue
                copy=self.Copy(possible_endings[i])
                copy[self.Index].act(copy,action,values)
                hash_copy=self.GetHash(self.current_state)
                if hash_copy in visited_nodes:
                    continue
                visited_nodes.add(hash_copy)
                possible_endings.append(copy)
                actions.append((i,(actions,values)))
            i+=1
        self.endings=possible_endings
        self.actions=actions
    
    def GetHash(self, Kingdoms:list[Kingdom])->str:
        hashes=[x.hash() for x in  Kingdoms]
        returnValue=""
        for h in hashes:
            returnValue+=h+'\n'
        return returnValue
    def Copy(self, Kingdoms:list[Kingdom])->list[Kingdom]:
        return [Kingdom(x) for x in Kingdoms]
    
    def moves(self, actions:list[tuple[int,tuple]], selection:int)->list[tuple]:
        if selection==0:
            return [actions[0][1]]
        moves=self.moves(actions,actions[selection][0])
        aux=moves[-1]
        moves[-1]=actions[selection][1]
        moves.append(aux)
        return moves