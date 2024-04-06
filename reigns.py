class Kingdom:

    #CONSTRUCTORS
    #-------------------------------------------------------
    def __init__(self):
        self.population=0
        self.walls=0
        self.army=[]
        self.available_troops=self.army
        self.available_moves=self.population
    
    def __init__(self,population:int,walls:int,army:int):
        self.population=population
        self.walls=walls
        self.army=[army]
        self.available_moves=self.population
        self.available_troops=[True]*len(self.army)
    
    def __init__(self,ToCopy):
        self.population=ToCopy.population
        self.walls=ToCopy.walls
        self.army=ToCopy.army
        self.available_moves=ToCopy.available_moves
        self.available_troops=ToCopy.available_troops
    #-------------------------------------------------------
    
    #OVERLOADABLED FUNCTIONS
    #---------------------------------------------------------------------------------
    
    #___________________________________
    def NewTurn(self):
        '''
            Start of the turn. Population raised and the troops are ready to fight
            Overload this function if you want to add something at the start of the turn
        '''
        self.population+=1
        self.available_moves=self.population
        self.available_troops=[True]*len(self.army)
    
    #___________________________________
    def actions(self, Kingdoms:list,current:int):
        '''
            Returns every options that the player has to play.
            Overload this function if it has a activation-call hability 
        '''

        for i in range(self.available_moves):
            yield ("Upgrade Walls",(current,i+1)) #ADD i LEVELS TO THE WALL

            yield ("Create Troop",(current,i+1)) #CREATE A TROOP LEVEL i

            for j in range(len(self.army)):
                yield ("Upgrade Troop",(current,j,i+1)) #ADD i LEVELS TO THE j TROOP

        for i in range(len(self.army)):
            if not self.available_troops[i]:
                continue
            for Kngdm in range(len(Kingdoms)):
                if Kngdm==current:
                    continue
                if (len(Kingdoms[Kngdm].army)==0):
                    if Kingdoms[Kngdm].walls==0:
                        if Kingdoms[Kngdm].population==0:
                            yield ("Attack King",(current,i,Kngdm)) #ATTACK THE KING WITH TROOP i
                        else:
                            yield ("Attack Popupation",(current,i,Kngdm)) #ATTACK THE POPULATION WITH TROOP i
                    else:
                        yield ("Attack Walls",(current,i,Kngdm)) #ATTACK THE WALLS WITH TROOP i
                else:
                    for j in range(len(Kingdoms[Kngdm].army)):
                        yield ("Attack Troop",(current,i,Kngdm,j)) #ATTACK AN ENEMY TROOP WITH TROOP i
        yield ("Pass",(current,))

    #___________________________________
    def act(self,Kingdoms:list,action:str,values:tuple):
        '''
            This method calls the specific actions to execute
            Overload this method if call an hability is a posible action
            returns: if a king was defeated
        '''
        
        king_defeated=False

        if(action=="Upgrade Walls"):
            self.UpdateWalls(values[1])        
        if(action=="Create Troop"):
            self.CreateTroop(values[1])
        if(action=="Upgrade Troop"):
            self.UpdateTroop(values[1],values[2])
        if(action=="Attack King"):
            self.AttackKing(values,Kingdoms)
            king_defeated=True
        if(action=="Attack Popupation"):
            self.AttackPopulation(values,Kingdoms)
        if(action=="Attack Walls"):
            self.AttackWalls(values,Kingdoms)
        if(action=="Attack Troop"):
            self.AttackTroop(values,Kingdoms)
            Kingdoms[values[2]].sort_troops()
        self.sort_troops()
        return king_defeated
    #___________________________________
    def UpdateWalls(self,value:int):
        '''
            This method upgadres the wall in 'value' levels
            Overload this method if a pasive hability is related with walls level ups
        '''
        self.available_moves-=value
        self.walls+=value

    #___________________________________
    def UpdateTroop(self,troop:int,value:int):
        '''
            This method upgadres the troop 'troop' in 'value' levels
            Overload this method if a hability is related with troop level ups
        '''
        self.available_moves-=value
        self.army[troop]+=value

    #___________________________________
    def CreateTroop(self,value:int):
        '''
            This method creates a troop in 'value' levels
            Overload this method if a hability is related with troops crations
        '''
        self.available_moves-=value
        self.army.append(value)
        self.available_troops.append(True)

    #___________________________________
    def AttackKing(self,values:tuple,Kingdoms:list):
        '''
            This method is used to attack an enemy's King
            values: (number of the attacker, troop number, number of King attacked)
            Overload this method if a hability is related with the attack of a king
        '''
        Kingdoms[values[2]].KingAttacked(Kingdoms,values[0],values[1])
        self.available_troops[values[1]]=False

    #___________________________________
    def KingAttacked(self,Kingdoms:list,attacker:int,troop_number:int):
        '''
            This method is went an enemy attacks your King
            Overload this method if a hability is related with the attack of your king
        '''
        pass

    #___________________________________
    def AttackPopulation(self,values,Kingdoms):
        '''
            This method is used to attack an enemy's population
            values: (number of the attacker, troop number, number of Kingdom attacked)
            Overload this method if a pasive hability is related with the attack of a population
        '''
        Kingdoms[values[2]].PopulationAttacked(Kingdoms,values[0],values[1])
        self.available_troops[values[1]]=False
    
    #___________________________________
    def PopulationAttacked(self,Kingdoms:list,attacker:int,troop_number:int):
        '''
            This method is went your population is under attack
            Overload this method if a hability is related with the attack of your population
        '''
        self.population-=Kingdoms[attacker].army[troop_number]
        if self.population<0:
            self.population=0
    
    #___________________________________
    def AttackWalls(self,values,Kingdoms):
        '''
            This method is used to attack an enemy's walls
            values: (number of the attacker, troop number, number of Kingdom attacked)
            Overload this method if a pasive hability is related with the attack of a walls
        '''
        Kingdoms[values[2]].WallsAttacked(Kingdoms,values[0],values[1])
        self.available_troops[values[1]]=False
    
    #___________________________________
    def WallsAttacked(self,Kingdoms:list,attacker:int,troop_number:int):
        '''
            This method is went your walls is under attack
            Overload this method if a hability is related with the attack of your walls
        '''
        self.walls-=Kingdoms[attacker].army[troop_number]//2
        if self.walls<0:
            self.walls=0
    
    #___________________________________
    def AttackTroop(self,values,Kingdoms):
        '''
            This method is used to attack one of the enemy's troop
            values: (number of the attacker, troop number, number of Kingdom attacked, target troop)
            Overload this method if a hability is related with the attack of a troop
        '''
        Kingdoms[values[2]].TroopCombat(Kingdoms,values[0],values[1],values[3])
        self.available_troops[values[1]]=False
        self.CheckTroop(values[1])
    
    #___________________________________
    def TroopCombat(self,Kingdoms:list,attacker:int,troop_number:int,target:int):
        '''
            This method is called went you suffer an enemy attack to one of your troops
            Overload this method if a hability is related went the enemy attacks you
        '''
        if(self.army[target]<Kingdoms[attacker].army[troop_number]):
            Kingdoms[attacker].army[troop_number]-=(self.army[target]+1)//2
            self.army[target]=0
        elif (self.army[target]<Kingdoms[attacker].army[troop_number]):
            Kingdoms[attacker].army[troop_number]=0
            self.army[target]=(Kingdoms[attacker].army[troop_number]+1)//2
        else:
            self.army[target]=0
            Kingdoms[attacker].army[troop_number]=0
        self.CheckTroop(target)

    #___________________________________
    def CheckTroop(self,target):
        '''
        This method manage the destruction of a troop
        '''
        if self.army[target]==0:
            self.army.pop(target)
            self.available_troops.pop(target)
    
    #___________________________________
    def sort_troops(self):
        '''
        This method sort the troops. First the available and then those who are not available
        '''
        troops=[x for x in zip(self.available_troops,self.army)]
        troops=sorted(troops,key=lambda x:x[1] if x[0] else -1.0/x[1], reverse=True)
        self.available_troops=[x[0] for x in troops]
        self.army=[x[1] for x in troops]

    #_____________________________________
    def hash(self)->str:
        returnValue = f"{self.population}/{self.walls}/{self.available_moves}"
        for i in range(len(self.army)):
            returnValue=returnValue+f"{self.army[i]}{self.available_troops[i]}"
        return returnValue
    #---------------------------------------------------------------------------------