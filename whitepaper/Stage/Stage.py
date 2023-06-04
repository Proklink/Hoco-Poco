from Stage.Substage import Substage
from InternalEvents import set_handler

class Stage(Substage):
    def __init__(self):
        self.stages: list
        self.current: int


class DiceThrowing(Stage):

    def __init__(self):
        set_handler("dice", self.dice)

    def set_dice(self, dice):
        self.dice = dice
    pass