from src.Simulation_Model.Reigns import Kingdom


class Knowledge_Base:
    def __init__(self):
        self.strategy = None

        self.current_state = None
        self.Index = None
        self.endings = None
        self.actions = None

        self.reels = None
        self.alliance = None

    def Learn(self, sentence, Info: dict):
        if sentence == "strategy":
            self.strategy = Info["strategy"]
        if sentence == "number of kingdoms":
            self.reels = [-1] * Info["number"]
            self.alliance = [0] * Info["number"]
        if sentence == "current state":
            self.current_state = Info["state"]
            self.Index = Info["Index"]
        if sentence == "attack made":
            if Info["defender"] == self.Index:
                if Info["objetive"] == "Troop":
                    self.reels[Info["attacker"]] -= 3
                elif Info["objetive"] == "Walls":
                    self.reels[Info["attacker"]] -= 5
                elif Info["objetive"] == "Population":
                    self.reels[Info["attacker"]] -= 10
                if self.alliance[Info["attacker"]] > 0:
                    self.alliance[Info["attacker"]] = 0
                    self.reels[Info["attacker"]] -= 50
            elif self.reels[Info["defender"]] > 0:
                self.reels[Info["attacker"]] -= 1
            elif self.reels[Info["defender"]] < 0:
                self.reels[Info["attacker"]] += 1
            if Info["attacker"] == self.Index:
                self.alliance[Info["defender"]] = 0
        if sentence == "alliance answer":
            if Info["answer"]:
                self.alliance[Info["reign"]] = 3
                self.reels[Info["reign"]] += 5
            else:
                self.reels[Info["reign"]] -= 1
        if sentence == "end of the turn":
            for x in range(len(self.alliance)):
                if self.alliance[x] > 0:
                    self.alliance -= 1

    def Think(self, query: str, Info: dict = dict()):
        if query == "possible endings":
            self.possible_endings()
            return self.endings
        if query == "best ending":
            return self.strategy.Select(
                self.Index, Info["endings"], self.reels, self.alliance
            )
        if query == "actions for best ending":
            return self.moves(self.actions, Info["selection"])
        if query == "possible allies":
            alliance_proposal = self.strategy.ChooseAllies(
                self.current_state, self.Index, self.reels, self.alliance
            )
            alliance_proposal = [
                alliance_proposal[i] and self.alliance[i] == 0
                for i in range(len(self.alliance))
            ]
            alliance_proposal[self.Index] = False
            return alliance_proposal
        if query == "accept alliance":
            accept = self.strategy.AcceptAlliance(
                self.current_state, self.Index, Info["reign"], self.reels, self.alliance
            )
            if accept:
                self.alliance[Info["reign"]] = 3
                self.reels[Info["reign"]] += 3
            return accept

    def possible_endings(self):
        visited_nodes = set()
        visited_nodes.add(self.GetHash(self.current_state))
        possible_endings = [self.Copy(self.current_state)]
        actions = [(0, ("Pass", (self.Index,)))]
        i = 0
        while i < len(possible_endings):
            for action, values in possible_endings[i].actions(
                possible_endings[i], self.Index
            ):
                if action == "Pass":
                    continue
                copy = self.Copy(possible_endings[i])
                copy[self.Index].act(copy, action, values)
                hash_copy = self.GetHash(self.current_state)
                if hash_copy in visited_nodes:
                    continue
                visited_nodes.add(hash_copy)
                possible_endings.append(copy)
                actions.append((i, (actions, values)))
            i += 1
        self.endings = possible_endings
        self.actions = actions

    def GetHash(self, Kingdoms: list[Kingdom]) -> str:
        hashes = [x.hash() for x in Kingdoms]
        returnValue = ""
        for h in hashes:
            returnValue += h + "\n"
        return returnValue

    def Copy(self, Kingdoms: list[Kingdom]) -> list[Kingdom]:
        return [
            Kingdom(army=x.army, population=x.population, walls=x.walls)
            for x in Kingdoms
        ]

    def moves(self, actions: list[tuple[int, tuple]], selection: int) -> list[tuple]:
        if selection == 0:
            return [actions[0][1]]
        moves = self.moves(actions, actions[selection][0])
        aux = moves[-1]
        moves[-1] = actions[selection][1]
        moves.append(aux)
        return moves
