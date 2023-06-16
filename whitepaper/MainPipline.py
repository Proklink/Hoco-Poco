from Stage.Stage import *
from Stage.Substage import *
from Player import Player
import random, time
from InternalEvents import set_handler

random.seed(int(time.time()))


class MainPipline():
    def __init__(self, number_of_players = 2):
        self.number_of_players = number_of_players
        self.listeners = [{}, {}, {}, {}] #listeners: [{dice number: {player id: {card id : number of cards}}}]

        self.players = [Player("1"), Player("2")]
        self.players[0].add_card(0, CardType.GREEN, self.subscribe)
        self.players[1].add_card(1, CardType.GREEN, self.subscribe)
        self.current_stage = 0
        self.access_to_continue = True
        self.dice = 0

        set_handler("update_continuation", self.update_continuation)
        set_handler("dice", self.set_dice)
        set_handler("new_grafics", self.not_continue)
        set_handler("new_dialog", self.not_continue)

        self.stages = [ActivePlayerSetter(self.players),
                       DiceThrowing(),
                       RedCards(self.players, self.listeners),
                       BlueCards(self.players, self.listeners),
                       GreenCards(self.players, self.listeners)]
        

    def subscribe(self, dice_list, card, player: int, color: CardType):
        for dice in dice_list:
            listeners_item = self.listeners[color.value].get(dice)
            
            if not listeners_item:
                self.listeners[color.value][dice] = {player : {card.id : 1}}
            else:
                player_cards = listeners_item.get(player)

                if not player_cards:
                    listeners_item[player] = {card.id : 1}
                else:
                    card_num = player_cards.get(card.id)
                    if card_num:
                        player_cards[card.id] += 1
                    else:
                        player_cards[card.id] = 1

    def unsubscribe(self, dice_list, card, player: int, color: CardType):
        for dice in dice_list:
            listeners_item = self.listeners[color.value].get(dice)
            
            if listeners_item:
                player_cards = listeners_item.get(player)

                if player_cards:
                    card_id = player_cards.get(card.id)
                    if card_id:
                        del player_cards[card.id]

    def not_continue(self, new_gobjects):
        self.access_to_continue = False

    def set_dice(self, dice):
        self.dice = dice

    def update_continuation(self):
        self.access_to_continue = True

    def update(self):
        if self.stages[self.current_stage].is_ended():
            self.current_stage += 1
            self.current_stage %= len(self.stages)
        if self.current_stage == 0:
            for stage in self.stages:
                stage.reset()

    def run(self):
        if self.access_to_continue:
            self.stages[self.current_stage].run()
        return []