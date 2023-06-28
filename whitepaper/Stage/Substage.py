from abc import ABC, abstractmethod
from Graphics.GInfo import *
from cards import CardType
import cards as crds
from InternalEvents import dispatch_event, set_handler
from enum import Enum
import random

class Substage(ABC):

    @abstractmethod
    def run(self):
        pass

class substage_wrapper(Substage):
    def __init__(self, wrapped_tuple) -> None:
        super().__init__()
        self.logic_func = wrapped_tuple[0]
        self.arg_list = wrapped_tuple[1]

    def run(self):
        self.logic_func(self.arg_list)

class ActivePlayerSetter(Substage):

    def __init__(self, players: list):
        super().__init__()
        self.active_player_id = -1
        self.number_of_players = len(players)
        self.players = players
        self.ended = False
        set_handler('turn', self.turn)
        self.one_more_turn = False

    def turn(self):
        self.one_more_turn = True
        
    def run(self):
        if not self.one_more_turn:
            self.active_player_id += 1
            self.active_player_id %= self.number_of_players
            self.one_more_turn = False
        dispatch_event('new_grafics', [ (NotificationExpired, ['Ход игрока {}'.format(self.players[self.active_player_id].name), 1, [], "update_continuation"])])
        dispatch_event('active_player', self.players[self.active_player_id])
        self.ended = True
    
    def reset(self):
        self.ended = False
    
    def is_ended(self):
        if self.ended == False:
            return self.ended
        else:
            self.ended = False
            return True
    
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
            dispatch_event('new_grafics', [ (NotificationExpired, ['Игрок бросает один кубик', 1, [], "update_continuation"]) ])
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
            dispatch_event('new_grafics', [ (NotificationExpired, ['Игрок выбросил кубики ({} : {})'.format(first, second), 1, [], "update_continuation"]) ])
            dispatch_event('dice', [first + second, first, second])
        else:
            dispatch_event('new_grafics', [ (NotificationExpired, ['Игрок выбросил кубик ({})'.format(first), 1, [], "update_continuation"]) ])
            dispatch_event('dice', [first])


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


class prepare_and_check_reds(Substage):
    def __init__(self, listeners):
        self.listeners = listeners
        set_handler('dice', self.new_dice)
        set_handler("active_player", self.new_active_player)
        self.temp_players = []

    def new_active_player(self, active_player):
        self.active_player = active_player

    def new_dice(self, dice):
        self.dice = dice[0]

    def run(self):
        reds = self.listeners[CardType.RED.value].get(self.dice)
        if reds is None:
            print('red_end')
            dispatch_event('red_end')
            return

        if self.active_player.money == 0:
            dispatch_event('new_grafics', [ (NotificationExpired, ['У игрока {} нет денег'.format(self.active_player.name), 1, [], "update_continuation"]) ])
            dispatch_event('red_end')
            return
        
        self.temp_players = []

        reds_list = list(reds.items())
        reds_list.reverse()
        for player_id, cards in reds_list:
            if player_id != self.active_player.id:
                self.temp_players.append((player_id, cards))
        
        if self.temp_players == []:
            print('red_end')
            dispatch_event('red_end')
        else:
            print('stages_red')
            dispatch_event('stages_red', self.temp_players)


class process_player_red(Substage):
    def __init__(self, players):
        self.players = players
        self.current = 0
        set_handler("active_player", self.new_active_player)
        set_handler("stages_red", self.stages_red)

    def stages_red(self, temp_players):
        self.temp_players = temp_players

    def new_active_player(self, active_player):
        self.active_player = active_player

    def run(self):
        tc = ''
        player_id = self.temp_players[self.current][0]
        cards = self.temp_players[self.current][1]

        card_id, number = list(cards.items())[0]
        card_profit = crds.red_cards[card_id].profit

        #проверяем наличие карты Торговый центр
        if self.players[player_id].cards[CardType.WIN.value].get(1) != None and \
                card_id in crds.win_cards[1].depends[CardType.RED.value]:
            card_profit += 1
            tc = ', учитывая Торговый центр'

        need_to_pay = number * card_profit

        if self.active_player.money == 0:
            res_str = 'У игрока {} нет денег'.format(self.active_player.name)
            print(res_str)
            dispatch_event('new_grafics', [ (NotificationExpired, [res_str, 1, [], "update_continuation"]) ])
            dispatch_event('red_end')
            return
        elif self.active_player.money < need_to_pay:
            res_str = "Игрок {} платит игроку {} {} монет за карту {}{}".format(self.active_player.name, self.players[player_id].name, self.active_player.money, crds.red_cards[card_id].name, tc)
            
            self.players[player_id].money += self.active_player.money
            self.active_player.money = 0

            print(res_str)
            dispatch_event('new_grafics', [ (NotificationExpired, [res_str, 1, [], "update_continuation"]) ])
            dispatch_event('red_end')
            return
        else:
            res_str = "Игрок {} платит игроку {} {} монет за карту {}{}".format(self.active_player.name, self.players[player_id].name, need_to_pay, crds.red_cards[card_id].name, tc)
            
            self.players[player_id].money += need_to_pay
            self.active_player.money -= need_to_pay

            print(res_str)
            dispatch_event('new_grafics', [ (NotificationExpired, [res_str, 1, [], "update_continuation"]) ])
        
        self.current += 1
        self.current %= len(self.temp_players)

        if self.current == len(self.temp_players) - 1:
            dispatch_event('red_end')
            return
        
class prepare_and_check_blues(Substage):
    def __init__(self, listeners, players):
        self.listeners = listeners
        self.players = players
        set_handler('dice', self.new_dice)
        set_handler("active_player", self.new_active_player)

    def new_active_player(self, active_player):
        self.active_player = active_player

    def new_dice(self, dice):
        self.dice = dice[0]

    def run(self):
        blues = self.listeners[CardType.BLUE.value].get(self.dice)
        if blues is None:
            dispatch_event('blue_end')
            return
        
        stages = []

        for player_id, cards in blues.items():
            card_id, number = list(cards.items())[0]
            
            def substage(arg_list):
                player_id = arg_list[0]
                number = arg_list[1]
                card_id = arg_list[2]

                need_to_pay = number * crds.blue_cards[card_id].profit
                res_str = "Игрок {} получает {} монет из банка за карту {}".format(self.active_player.name, need_to_pay, crds.blue_cards[card_id].name)
                print(res_str)
                dispatch_event('new_grafics', [ (NotificationExpired, [res_str, 1, [], "update_continuation"]) ])
            
                self.players[player_id].money += need_to_pay

            stages.append(substage_wrapper((substage, [player_id, number, card_id])))

        if stages == []:
            dispatch_event('blue_end')
        else:
            stages.append(substage_wrapper((lambda l: dispatch_event('blue_end'), [])))
            dispatch_event('stages_blue', stages)

class greens(Substage):
    def __init__(self, listeners, players):
        self.listeners = listeners
        self.players = players
        set_handler('dice', self.new_dice)
        set_handler("active_player", self.new_active_player)

    def new_active_player(self, active_player):
        self.active_player = active_player

    def new_dice(self, dice):
        self.dice = dice[0]

    def run(self):
        greens = self.listeners[CardType.GREEN.value].get(self.dice)
        if not greens:
            dispatch_event('green_end')
            return
        
        green_cards = greens.get(self.active_player.id)
        if not green_cards:
            dispatch_event('green_end')
            return
        
        tc = ''
        green_card_id, green_card_number = list(green_cards.items())[0]
        card_profit = crds.green_cards[green_card_id].profit

        #проверяем наличие карты Торговый центр
        if self.players[self.active_player.id].cards[CardType.WIN.value].get(1) != None and \
                green_card_id in crds.win_cards[1].depends[CardType.GREEN.value]:
            card_profit += 1
            tc = ', учитывая Торговый центр'

        if crds.green_cards[green_card_id].depends == []:
            need_to_pay = card_profit
        else:
            need_to_pay = 0
            for blue_card_id in crds.green_cards[green_card_id].depends:
                blue_card_number = self.players[self.active_player.id].cards[CardType.BLUE.value].get(blue_card_id)

                if blue_card_number != None:
                    need_to_pay += blue_card_number * card_profit
        
        need_to_pay *= green_card_number
        res_str = "Игрок {} получает {} монет из банка за карту {}{}".format(self.active_player.name, need_to_pay, crds.green_cards[green_card_id].name, tc)
        print(res_str)
        dispatch_event('new_grafics', [ (NotificationExpired, [res_str, 1, [], "update_continuation"]) ])
        self.players[self.active_player.id].money += need_to_pay
        dispatch_event('green_end')

class telecenter(Substage):
    def __init__(self, listeners, players):
        self.listeners = listeners
        self.players = players
        self.last_clicked_player = -1
        self.last_card_clicked = ()
        self.need_to_run = False
        # set_handler("card", self.card_clicked)
        set_handler("player_clicked", self.player_clicked)
        set_handler("cancel_telecenter", self.cancel_telecenter)
        set_handler("apply_telecenter", self.apply_telecenter)
        set_handler("active_player", self.new_active_player)
        set_handler("telecenter", self.telecenter)

    def telecenter(self):
        self.need_to_run = True

    def new_active_player(self, active_player):
        self.active_player_id = active_player.id

    def apply_telecenter(self, _):
        need_to_pay = crds.purple_cards[2].profit
        other_player = self.players[self.last_clicked_player]
        active_player = self.players[self.active_player_id]

        if other_player.money == 0:
            res_str = 'У игрока {} нет денег'.format(other_player.name)

        elif other_player.money < need_to_pay:
            res_str = "Игрок {} платит игроку {} {} монет за карту {}".format(other_player.name, active_player.name, other_player.money, crds.purple_cards[2].name)
            
            active_player.money += other_player.money
            other_player.money = 0
        else:
            res_str = "Игрок {} платит игроку {} {} монет за карту {}".format(other_player.name, active_player.name, other_player.money, crds.purple_cards[2].name)
            
            active_player.money += need_to_pay
            other_player.money -= need_to_pay

        print(res_str)
        dispatch_event('new_grafics', [ (NotificationExpired, [res_str, 1, [], "update_continuation"]) ])
        self.need_to_run = False
        dispatch_event('purple_continue')
        

    def cancel_telecenter(self, _):
        dispatch_event('purple_continue')

    def player_clicked(self, player_id):
        if not self.need_to_run:
            return

        if player_id == self.active_player_id:
            dispatch_event('new_dialog', get_graphic_info_player_self())
        else:
            self.last_clicked_player = player_id
            dispatch_event('new_dialog', get_graphic_info_player_other(self.players[player_id].name))

    def run(self):
        if not self.need_to_run:
            dispatch_event('purple_continue')
            return
        dispatch_event('new_dialog', get_graphic_info_player_self())


class stadium(Substage):
    def __init__(self, listeners, players):
        self.listeners = listeners
        self.players = players
        self.last_clicked_player = -1
        self.last_card_clicked = ()
        self.need_to_run = False

        set_handler("active_player", self.new_active_player)
        set_handler("stadium", self.in_game)

    def in_game(self):
        self.need_to_run = True

    def new_active_player(self, active_player):
        self.active_player_id = active_player.id

    def run(self):
        if not self.need_to_run:
            dispatch_event('purple_continue')
            return
        
        card_id = 0
        need_to_pay = crds.purple_cards[card_id].profit

        active_player = self.players[self.active_player_id]

        for player in self.players:
            if player.id == active_player.id:
                continue
            if player.money == 0:
                continue
            elif player.money < need_to_pay:
                res_str = "Игрок {} платит игроку {} {} монет за карту {}".format(player.name, active_player.name, player.money, crds.purple_cards[card_id].name)
                self.players[active_player.id].money += player.money
                player.money = 0
                print(res_str)
                dispatch_event('new_grafics', [ (NotificationExpired, [res_str, 1, [], "update_continuation"]) ])
            else:
                res_str = "Игрок {} платит игроку {} {} монет за карту {}".format(player.name, active_player.name, need_to_pay, crds.purple_cards[card_id].name)
                self.players[active_player.id].money += need_to_pay
                player.money -= need_to_pay
                print(res_str)
                dispatch_event('new_grafics', [ (NotificationExpired, [res_str, 1, [], "update_continuation"]) ])
        self.need_to_run = False
        dispatch_event('purple_continue')


class prepare_and_check_purple(Substage):
    def __init__(self, listeners, players):
        self.listeners = listeners
        self.players = players
        set_handler('dice', self.new_dice)
        set_handler("active_player", self.new_active_player)

    def new_active_player(self, active_player):
        self.active_player = active_player

    def new_dice(self, dice):
        self.dice = dice[0]

    def run(self):
        purples = self.listeners[CardType.PURPLE.value].get(self.dice)
        if not purples:
            dispatch_event('purple_end')
            return
        
        purple_cards = purples.get(self.active_player.id)
        if not purple_cards:
            dispatch_event('purple_end')
            return

        for card_id, _ in purple_cards.items():
            if card_id == 0:    #взять деньги у всех (стадион)
                dispatch_event('stadium')
            elif card_id == 1:  #обмен картами (деловой центр)
                dispatch_event('busycenter')
            else:               #взять у одного игрока 5 монет
                dispatch_event('telecenter')

        dispatch_event('purple_continue')

class shop(Substage):
    def __init__(self, listeners, players):
        self.listeners = listeners
        self.players = players
        self.last_card_clicked = ()
        self.need_to_run = False

        set_handler("shop_in_game", self.in_game)
        set_handler("card", self.card_clicked)
        set_handler("cancel_shop", self.cancel_shop)
        set_handler("apply_shop", self.apply_shop)
        set_handler("active_player", self.new_active_player)

    def in_game(self):
        self.need_to_run = True

    def new_active_player(self, active_player):
        self.active_player_id = active_player.id

    def apply_shop(self, _):        
        need_to_pay = crds.cards_by_colors[self.last_card_clicked[0].value][self.last_card_clicked[1]].cost
        active_player = self.players[self.active_player_id]

        if active_player.money < need_to_pay:
            res_str = "У вас недостаточно монет для покупки {}".format(crds.cards_by_colors[self.last_card_clicked[0].value][self.last_card_clicked[1]].name)
            print(res_str)
            dispatch_event('new_grafics', [ (NotificationExpired, [res_str, 1, [], "update_continuation"]) ])
        else:
            res_str = "Игрок покупает карту {}".format(crds.cards_by_colors[self.last_card_clicked[0].value][self.last_card_clicked[1]].name)
            
            active_player.money -= need_to_pay
            dispatch_event('card_buy', self.active_player_id, self.last_card_clicked[0], self.last_card_clicked[1])

            print(res_str)
            dispatch_event('new_grafics', [ (NotificationExpired, [res_str, 1, [], "update_continuation"]) ])
            dispatch_event('shop_end')

    def cancel_shop(self, _):
        dispatch_event('shop_end')

    def card_clicked(self, color, card_id):
        if not self.need_to_run:
            return
        self.last_card_clicked = (color, card_id)

        dispatch_event('new_dialog', get_graphic_info_card(color, card_id))
            

    def run(self):
        if self.players[self.active_player_id].money == 0 or not self.need_to_run:
            dispatch_event('shop_end')
            return
        dispatch_event('new_dialog', get_graphic_info_shop())