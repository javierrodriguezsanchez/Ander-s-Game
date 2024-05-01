from src.Strategies.Strategy import Strategy
from src.Strategies.Implementations.utils.utils import Predict
from src.Strategies.Implementations.AlliesStrategy import AlliesStrategy
import random


class PredictStrategy(Strategy):
    """
    Make decisions accordin to his predictions for future
    """
    def __init__(self, base:Strategy=None):
        if base is None:
            base = AlliesStrategy()
        self.base=base

    def Select(self, context: dict) -> int: 
        new_context=context
        new_context['endings'] = Predict(context)
        return self.base.Select(context)

    def ChooseAllies(self, context: dict) -> list[bool]:
        return self.base.ChooseAllies(context)

    def AcceptAlliance(self, context: dict) -> bool:
        return self.base.ChooseAllies(context)
