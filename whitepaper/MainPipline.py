from Stage.Stage import *
from Stage.Substage import *

import random, time
from InternalEvents import set_handler

random.seed(int(time.time()))

class Continuation:
    def __init__(self):
        self.access_to_continue = True
        self.new_graphics_counter = 0
        set_handler("update_continuation", self.update_continuation)
        set_handler("new_grafics", self.not_continue)
        set_handler("new_dialog", self.not_continue)

    def not_continue(self, new_gobjects):
        self.new_graphics_counter += 1
        self.access_to_continue = False

    def update_continuation(self):
        self.new_graphics_counter -= 1
        if self.new_graphics_counter <= 0:
            self.access_to_continue = True
            self.new_graphics_counter = 0

    @property 
    def get(self): 
        return self.access_to_continue 

class MainPipline():
    def __init__(self, players):
        self.number_of_players = len(players)
        self.listeners = [{}, {}, {}, {}] #listeners: [{dice number: {player id: {card id : number of cards}}}]

        self.players = players

        self.players[0].add_card(0, CardType.BLUE, self.subscribe)
        # self.players[0].add_card(1, CardType.BLUE, self.subscribe)
        # self.players[0].add_card(2, CardType.BLUE, self.subscribe)
        # self.players[0].add_card(3, CardType.BLUE, self.subscribe)
        # self.players[0].add_card(4, CardType.BLUE, self.subscribe)

        self.players[0].add_card(0, CardType.GREEN, self.subscribe)
        # self.players[0].add_card(1, CardType.GREEN, self.subscribe)

        # self.players[0].add_card(3, CardType.GREEN, self.subscribe)
        # self.players[0].add_card(4, CardType.GREEN, self.subscribe)

        # self.players[0].add_card(1, CardType.RED, self.subscribe)
        # self.players[0].add_card(0, CardType.RED, self.subscribe)

        # self.players[0].add_card(0, CardType.PURPLE, self.subscribe)
        # self.players[0].add_card(1, CardType.PURPLE, self.subscribe)
        # self.players[0].add_card(2, CardType.PURPLE, self.subscribe)

        # self.players[0].add_card(0, CardType.WIN, self.subscribe)
        # self.players[0].add_card(1, CardType.WIN, self.subscribe)
        # self.players[0].add_card(2, CardType.WIN, self.subscribe)
        # self.players[0].add_card(3, CardType.WIN, self.subscribe)


        self.players[1].add_card(0, CardType.BLUE, self.subscribe)

        # self.players[1].add_card(2, CardType.BLUE, self.subscribe)
        # self.players[1].add_card(3, CardType.BLUE, self.subscribe)
        # self.players[1].add_card(4, CardType.BLUE, self.subscribe)

        self.players[1].add_card(0, CardType.GREEN, self.subscribe)
        # self.players[1].add_card(1, CardType.GREEN, self.subscribe)
        # self.players[1].add_card(2, CardType.GREEN, self.subscribe)
        # self.players[1].add_card(3, CardType.GREEN, self.subscribe)
        # self.players[1].add_card(4, CardType.GREEN, self.subscribe)

        # self.players[1].add_card(1, CardType.RED, self.subscribe)
        # self.players[1].add_card(0, CardType.RED, self.subscribe)

        # self.players[1].add_card(0, CardType.PURPLE, self.subscribe)
        # self.players[1].add_card(1, CardType.PURPLE, self.subscribe)
        # self.players[1].add_card(2, CardType.PURPLE, self.subscribe)

        # self.players[1].add_card(0, CardType.WIN, self.subscribe)
        # self.players[1].add_card(1, CardType.WIN, self.subscribe)
        # self.players[1].add_card(2, CardType.WIN, self.subscribe)
        # self.players[1].add_card(3, CardType.WIN, self.subscribe)

        set_handler('card_buy', self.card_buy)

        self.current_stage = 0
        self.continuation = Continuation()

        self.stages = [ActivePlayerSetter(self.players),
                       DiceThrowing(),
                       RedCards(self.players, self.listeners),
                       BlueCards(self.players, self.listeners),
                       GreenCards(self.players, self.listeners),
                       PurpleCards(self.players, self.listeners),
                       ShopStage(self.players, self.listeners),
                       VictoryCheck(self.players, self.listeners),
                       HappinessCheck(self.players, self.listeners)]
        
    def card_buy(self, player_id, color, card_id):
        self.players[player_id].add_card(card_id, CardType(color), self.subscribe)
        

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

    def update(self):
        if self.stages[self.current_stage].is_ended():
            self.current_stage += 1
            self.current_stage %= len(self.stages)
        # if self.current_stage == 0:
        #     print('reset')
        #     for stage in self.stages:
        #         stage.reset()
                

    def run(self):
        if self.continuation.get:
            self.stages[self.current_stage].run()
        return []