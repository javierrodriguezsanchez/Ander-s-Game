class Strategy:
    def __init__(self):
        pass

    def Select(self, context: dict) -> int:
        pass

    def ChooseAllies(self, context: dict) -> list[bool]:
        return [False] * len(context['state'])

    def AcceptAlliance(self, context: dict) -> bool:
        return False