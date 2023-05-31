import random, time
from Player import Player
from cards import CardType
import cards as crds
from DiceManager import DiceManager
import BuildManager

random.seed(int(time.time()))

players = [Player('0'), Player('1')]#, Player('2')]

def dice_throwing():
    first = random.randint(1, 6)
    second = random.randint(1, 6)
    return first, second

dice_manager = DiceManager()

players[0].add_card(0, CardType.BLUE, dice_manager.subscribe)
players[0].add_card(0, CardType.GREEN, dice_manager.subscribe)

players[1].add_card(0, CardType.BLUE, dice_manager.subscribe)
players[1].add_card(0, CardType.GREEN, dice_manager.subscribe)

count = 0
was_rethrowing = False
while True:
    player = players[count]
    print("player {} now have {} money".format(0, players[0].money))
    print("player {} now have {} money".format(1, players[1].money))
    print("-----------------------------------------------------------------------------------------------------------------")
    print("\nХод игрока {}\n".format(player.name))
    dice_tuple = dice_throwing()

    ans = 'n'
    if player.cards[CardType.WIN.value].get(crds.win_cards[0].id) != None:
        ans = input("Бросаете два кубика или один? 'y' - 2 кубика, 'n' - 1 кубик: ")
    if ans == 'y':
        dice = dice_tuple[0] + dice_tuple[1]
        print("\nИгрок выбросил кубики ({}-{}) на сумму {}\n".format(dice_tuple[0], dice_tuple[1], dice))
    else:
        # dice = dice_tuple[0]
        dice = 7
        print("\nИгрок выбросил кубик {}\n".format(dice))
    
    if player.cards[CardType.WIN.value].get(crds.win_cards[3].id) != None and not was_rethrowing:
        ans = input("Хотите перебросить кубики? 'y' - да, 'n' - нет: ")
        if ans == 'y':
            was_rethrowing = True
            continue

    #можно улучшить эти 4 строки так как цвет карт теперь в enum
    dice_manager.process_dice_red(dice, player, players)

    dice_manager.process_dice_blue(dice, players)
    
    dice_manager.process_dice_green(dice, player.id, players)

    dice_manager.process_dice_purple(dice, player.id, players)

    BuildManager.building(player, players, dice_manager.subscribe)

    
    if len(player.cards[CardType.WIN.value]) == 4:
        print('\nИгрок {} выиграл!'.format(player.name))
        break
    if player.cards[CardType.WIN.value].get(crds.win_cards[2].id) != None and dice_tuple[0] == dice_tuple[1]:
        print('\nИгрок ходит ещё раз')
    else:
        count+=1
        count = count % len(players)
    was_rethrowing = False