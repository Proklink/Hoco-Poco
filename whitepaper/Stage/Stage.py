from Stage.Substage import *
from InternalEvents import set_handler

class Stage(Substage):
    def __init__(self):
        self.stages: list
        self.current: int


class DiceThrowing(Stage):

    def __init__(self):
        set_handler("dice", self.set_dice)
        set_handler("dice_number", self.new_dice_number)
        set_handler("radiotower", self.radiotower)
        self.stages = [check_railway(), generate_dice(), check_radio_tower()]
        self.current = 0
        self.ended = False
    
    def radiotower(self, is_reroll):
        self.ended = not is_reroll
        if is_reroll:
            dispatch_event('new_grafics', [ (NotificationExpired, ['Игрок перебрасывает кубики ', 2, [], "update_continuation"]) ])


    def new_dice_number(self, dice_number):
        self.dice_number = dice_number

    def set_dice(self, dice):
        self.dice = dice
    
    def run(self):
        self.stages[self.current].run()

        self.current += 1
        self.current %= len(self.stages)

    def reset(self):
        self.ended = False
        self.stages = [check_railway(), generate_dice(), check_radio_tower()]

    def is_ended(self):
        return self.ended
