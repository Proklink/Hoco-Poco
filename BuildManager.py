from cards import CardType
import cards as Card_file
from Player import Player, print_cards_player, print_cards_market


def building(active_player: Player, players: list, subscribe):
    if active_player.money == 0:
        return

    while True:
        print("\nУ вас в наличии монет: {}".format(active_player.money))

        ans = input("\nВведите цвет карты (RED = 0, BLUE = 1, GREEN = 2, PURPLE = 3, WIN = 4), 'c' для отображения всех карт, 's' для отображения своих карт, 'o' для отображения карт другого игрока или 'n' для отмены: ")
        if ans == 'n':
            return
        elif ans == 'c':
            print_cards_market(active_player)
            continue
        elif ans == 's':
            print_cards_player(active_player)
            continue
        elif ans == 'o':
            other_player_id = int(input("\nВведите id другого игрока: "))
            print_cards_player(players[other_player_id])
            continue

        color = int(ans)
        choosen_card_id = int(input("\nВведите id карты: "))
        if color == CardType.WIN.value and active_player.cards[color].get(choosen_card_id) != None:
            print('У вас уже есть такая карта победы, попробуйте заново')
            continue

        need_to_pay = Card_file.cards_by_colors[color][choosen_card_id].cost

        if active_player.money < need_to_pay:
            print("У вас недостаточно монет")
            continue
        else:
            active_player.money -= need_to_pay
            print("\npay player {} now have {} money".format(active_player.id, active_player.money))
        active_player.add_card(choosen_card_id, CardType(color), subscribe)
        return