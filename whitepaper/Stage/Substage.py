from abc import ABC, abstractmethod
from Graphics.GInfo import *
from cards import CardType
import cards as crds
from InternalEvents import dispatch_event, set_handler
import random

class Substage(ABC):

    @abstractmethod
    def run(self):
        pass



class ActivePlayerSetter(Substage):

    def __init__(self, players: list):
        super().__init__()
        self.active_player_id = -1
        self.number_of_players = len(players)
        self.players = players
        self.ended = False
        
    def run(self):
        self.active_player_id += 1
        self.active_player_id %= self.number_of_players
        dispatch_event('new_grafics', [ (NotificationExpired, ['Ход игрока {}'.format(self.players[self.active_player_id].name), 2, [], "update_continuation"])])
        dispatch_event('active_player', self.players[self.active_player_id])
        self.ended = True
        return self.active_player_id
    
    def reset(self):
        self.ended = False
    
    def is_ended(self):
        return self.ended
    
class check_railway(Substage):
    def __init__(self):
        set_handler("active_player", self.new_active_player)
        self.active_player = None
    
    def new_active_player(self, active_player):
        self.active_player = active_player

    def run(self):
        if self.active_player.cards[CardType.WIN.value].get(crds.win_cards[0].id) != None:
            dispatch_event('new_dialog', get_railway_check_dialog())
        else:
            dispatch_event('new_grafics', [ (NotificationExpired, ['Игрок бросает один кубик', 2, [], "update_continuation"]) ])
            dispatch_event('dice_number', 1)


class generate_dice(Substage):
    def __init__(self):
        set_handler("dice_number", self.new_dice_number)

    def new_dice_number(self, new_dice_number):    
        self.dice_number = new_dice_number

    def run(self):
        first = random.randint(1, 6)
        second = random.randint(1, 6)
        if self.dice_number == 2:
            dispatch_event('new_grafics', [ (NotificationExpired, ['Игрок выбросил кубики ({} : {})'.format(first, second), 2, [], "update_continuation"]) ])
            dispatch_event('dice', (first + second, first, second))
        else:
            dispatch_event('new_grafics', [ (NotificationExpired, ['Игрок выбросил кубик ({})'.format(first), 2, [], "update_continuation"]) ])
            dispatch_event('dice', (first))


class check_radio_tower(Substage):
    def __init__(self):
        self.was_rethrowing = False
        set_handler("active_player", self.new_active_player)
        self.active_player = None
    
    def new_active_player(self, active_player):
        self.active_player = active_player

    def run(self):
        if self.active_player.cards[CardType.WIN.value].get(crds.win_cards[3].id) != None and not self.was_rethrowing:
            self.was_rethrowing = True
            dispatch_event('new_dialog', get_radiotower_check_dialog())
        else:
            dispatch_event('radiotower', False)
