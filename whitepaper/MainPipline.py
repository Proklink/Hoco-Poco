from Stage.Stage import Stage
from Stage.Substage import ActivePlayerSetter
from Player import Player
import random, time
from InternalEvents import set_handler

random.seed(int(time.time()))


class MainPipline():
    def __init__(self, number_of_players = 2):
        self.number_of_players = number_of_players
        self.players = [Player("1"), Player("2")]
        self.stages = [ActivePlayerSetter(self.players)]
        self.current_stage = 0

        self.access_to_continue = True

        self.dice = 0
        
        self.listeners = [{}, {}, {}, {}] #listeners: [{dice number: {player id: {card id : number of cards}}}]

        set_handler("update_continuation", self.update_continuation)
        set_handler("dice", self.set_dice)

    def set_dice(self, dice):
        self.dice = dice

    def update_continuation(self):
        self.access_to_continue = True

    def update(self):
        if self.stages[self.current_stage].is_ended():
            self.current_stage += 1
            self.current_stage %= len(self.stages)

    def run(self):
        if self.access_to_continue:
            grapfic_objects = self.stages[self.current_stage].run()

            if len(grapfic_objects) != 0:
                self.access_to_continue = False
                return grapfic_objects
        return []