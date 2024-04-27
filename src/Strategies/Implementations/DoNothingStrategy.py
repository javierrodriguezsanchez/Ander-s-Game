from src.Strategies.Strategy import Strategy
import random

class DoNothingStrategy(Strategy):
    '''
    Its hard to explain this one :(
    '''

    def Select(self, context: dict) -> int:
        return 0

    def ChooseAllies(self, context: dict) -> list[bool]:
        Kingdoms = context['state']
        return [False] * len(Kingdoms)

    def AcceptAlliance(self, context: dict) -> bool:
        prop_index = context['reign']
        reels = context['relations']

        if reels[prop_index] >= 10:
            return True
        elif reels[prop_index] > 0:
            rand = random.random()
            if rand < 0.5:
                return True
            else:
                return False
        else:
            return False