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
        # self.stages = [check_railway(), generate_dice(), check_radio_tower()]#проблема бага здесь

    def is_ended(self):
        #Это нужно, чтобы когда Этап завершит свою работу он вернул True, но
        #сразу стал готов для следующего запуска 
        if self.ended == False:
            return self.ended
        else:
            self.ended = False
            return True
    

class RedCards(Stage):
    def __init__(self, players, listeners):
        self.ended = False
        set_handler("red_end", self.red_end)
        self.stages = [prepare_and_check_reds(listeners), process_player_red(players)]
        self.current = 0

    def red_end(self):
        self.ended = True

    def is_ended(self):
        if self.ended == False:
            return self.ended
        else:
            self.ended = False
            self.current = 0
            return True

    def run(self):
        print('red run ', self.current)
        self.stages[self.current].run()

        if self.current == 0:
            self.current = 1

    def reset(self):
        self.ended = False
        self.current = 0


class BlueCards(Stage):
    def __init__(self, players, listeners):
        self.ended = False
        set_handler("blue_end", self.blue_end)
        set_handler("stages_blue", self.stages_blue)
        self.preparing = prepare_and_check_blues(listeners, players)
        self.stages = [self.preparing]
        self.current = 0

    def blue_end(self):
        self.ended = True

    def is_ended(self):
        if self.ended == False:
            return self.ended
        else:
            self.ended = False
            self.current = 0
            return True
    
    def stages_blue(self, stages):
        self.stages = [self.preparing]
        for stage in stages:
            self.stages.append(stage)

    def run(self):
        self.stages[self.current].run()

        self.current += 1
        self.current %= len(self.stages)

    def reset(self):
        self.ended = False
        self.current = 0

class GreenCards(Stage):
    def __init__(self, players, listeners):
        self.ended = False
        set_handler("green_end", self.green_end)
        self.stages = [greens(listeners, players)]
        self.current = 0

    def green_end(self):
        self.ended = True

    def is_ended(self):
        if self.ended == False:
            return self.ended
        else:
            self.ended = False
            self.current = 0
            return True

    def run(self):
        self.stages[self.current].run()

    def reset(self):
        self.ended = False
        self.current = 0

class PurpleCards(Stage):
    def __init__(self, players, listeners):
        self.ended = False
        set_handler("purple_end", self.purple_end)
        set_handler("purple_continue", self.purple_continue)
        self.preparing = prepare_and_check_purple(listeners, players)
        self.stages = [prepare_and_check_purple(listeners, players),
                       stadium(listeners, players),
                       telecenter(listeners, players)]
        self.current = 0

    def purple_end(self):
        self.ended = True

    def purple_continue(self):
        self.current += 1
        self.current %= len(self.stages)
        if self.current == 0:
            self.ended = True

    def is_ended(self):
        if self.ended == False:
            return self.ended
        else:
            self.ended = False
            self.current = 0
            return True

    def run(self):
        self.stages[self.current].run()

    def reset(self):
        self.ended = False
        self.current = 0

class ShopStage(Stage):
    def __init__(self, players, listeners):
        self.ended = False
        set_handler("shop_end", self.shop_end)
        self.stages = [shop(listeners, players)]
        self.current = 0

    def shop_end(self):
        self.ended = True

    def is_ended(self):
        if self.ended == False:
            return self.ended
        else:
            self.ended = False
            self.current = 0
            return True

    def run(self):
        dispatch_event('shop_in_game')
        self.stages[self.current].run()

        # self.current += 1
        # self.current %= len(self.stages)

    def reset(self):
        self.ended = False
        self.current = 0

class VictoryCheck(Stage):
    def __init__(self, players, listeners):
        self.ended = False
        set_handler("active_player", self.new_active_player)

    def new_active_player(self, active_player):
        self.active_player = active_player

    def is_ended(self):
        if self.ended == False:
            return self.ended
        else:
            self.ended = False
            return True

    def run(self):
        if len(self.active_player.cards[CardType.WIN.value]) == 4:
            res_str = 'Игрок {} выиграл!'.format(self.active_player.name)
            print(res_str)
            dispatch_event('new_grafics', [ (NotificationExpired, [res_str, 1, [], "game_over"]) ])
        self.ended = True

    def reset(self):
        self.ended = False

class HappinessCheck(Stage):
    def __init__(self, players, listeners):
        self.ended = False
        set_handler("active_player", self.new_active_player)
        set_handler('dice', self.new_dice)

    def new_dice(self, dice):
        self.dice = dice

    def new_active_player(self, active_player):
        self.active_player = active_player

    def is_ended(self):
        if self.ended == False:
            return self.ended
        else:
            self.ended = False
            return True

    def run(self):
        if len(self.dice) > 1 and self.dice[1] == self.dice[2] and \
           self.active_player.cards[CardType.WIN.value].get(crds.win_cards[2].id) != None:
            
            res_str = 'Игрок {} ходит ещё раз'.format(self.active_player.name)
            print(res_str)
            dispatch_event('new_grafics', [ (NotificationExpired, [res_str, 1, [], "update_continuation"]) ])
            dispatch_event('turn')
        self.ended = True

    def reset(self):
        self.ended = False
