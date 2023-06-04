from abc import ABC, abstractmethod
from Graphics.GInfo import NotificationExpired
from cards import CardType
import cards as crds

class Substage(ABC):

    @abstractmethod
    def run(self):
        pass



class ActivePlayerSetter(Substage):

    def __init__(self, players: list):
        super().__init__()
        self.active_player = 0
        self.number_of_players = len(players)
        self.players = players
        
    def run(self):
        self.active_player += 1
        self.active_player %= self.number_of_players

        return [ (NotificationExpired, ['Ход игрока {}'.format(self.players[self.active_player].name), 2, [], "update_continuation"])]
    
    def is_ended(self):
        return True
    
class check_railway(Substage):
    def __init__(self, active_player):
        self.active_player = active_player
        

    def run(self):
        ans = 'n'
        # if self.active_player.cards[CardType.WIN.value].get(crds.win_cards[0].id) != None:
        #     ans = input("Бросаете два кубика или один? 'y' - 2 кубика, 'n' - 1 кубик: ")
        # if ans == 'y':
        #     dice_number = 2
        #     print("\nИгрок выбросил кубики ({}-{}) на сумму {}\n".format(dice_tuple[0], dice_tuple[1], dice))
        # else:
        #     # dice = dice_tuple[0]
        #     dice = 7
        #     print("\nИгрок выбросил кубик {}\n".format(dice))


class generate_dice(Substage):
    def run(self):
        pass


class check_radio_tower(Substage):
    def run(self):
        pass
