from cards import CardType
import cards as card_file
# from tabulate import tabulate

class Player:
    __player_numbers = 0
    def __init__(self, name):
        self.money = 3
        self.name = name
        self.id = Player.__player_numbers
        self.cards = [{}, {}, {}, {}, {}]
        Player.__player_numbers += 1

    def add_card(self, card_id, color: CardType, subscribe):
        colored_cards = self.cards[color.value]
        number = colored_cards.get(card_id)
        if number != None:
            colored_cards[card_id] += 1
        else:
            colored_cards[card_id] = 1
        if color.value != CardType.WIN.value:
            card = card_file.cards_by_colors[color.value][card_id]
            subscribe(card.dice, card, self.id, color)

    def del_card(self, card_id, color: CardType, unsubscribe):
        colored_cards = self.cards[color.value]
        number = colored_cards.get(card_id)
        if number != None:
            if colored_cards[card_id] > 1:
                colored_cards[card_id] -= 1
            else:
                del colored_cards[card_id]
        if color.value != CardType.WIN.value:
            card = card_file.cards_by_colors[color.value][card_id]
            unsubscribe(card.dice, card, self.id, color)

def print_cards_market(active_player: Player):
    print("\nИмеющиеся карты в магазине: ")
    data = []
    wins = ["WIN: "]
    for card_id, card in card_file.win_cards.items():
        id = active_player.cards[CardType.WIN.value].get(card_id)
        if id == None:
            card = card_file.win_cards[card_id]
            wins.append("\n{} {} {}\n {}".format(CardType.WIN.name, card_id, card.name, card.descr))
    data.append(wins)

    for color in range(CardType.GREEN.value + 1):
        _cards = [CardType(color).name + ": "]
        for card_id, card in card_file.cards_by_colors[color].items():
            _cards.append("\n{} {} {}\n Dice {} Cost {}".format( CardType.RED.name, card_id, card.name, card.dice, card.cost))
        data.append(_cards)

    purples = ["PURPLE: "]
    for card_id, card in card_file.purple_cards.items():
        if active_player.cards[CardType.PURPLE.value].get(card_id):
            continue
        purples.append("\n{} {} {}\n Dice {} Cost {}".format( CardType.PURPLE.name, card_id, card.name, card.dice, card.cost))
    data.append(purples)

    # print(tabulate(data))

def print_player_cards_by_color(player, color: CardType, gap: str):
    mass = [color.name + ": "]
    for card_id, number in player.cards[color.value].items():
        card = card_file.cards_by_colors[color.value][card_id]
        mass.append("{}{} {} {} (x{})\n Dice {} Cost {}".format(gap, color.name, card_id, card.name, number, card.dice, card.cost))
    return mass

def print_win_cards(player: Player):
    mass = ['WIN: ']
    for card_id, number in player.cards[CardType.WIN.value].items():
        card = card_file.win_cards[card_id]
        mass.append("\n{} {}\n {}".format(card_id, card.name, card.descr))
    return mass

def print_cards_player(player: Player):
    print("\nИгрок {} (id {}) имеет {} монет и следующие карты: ".format(player.name, player.id, player.money))

    data = []
    wins = print_win_cards(player)
    if len(wins) > 1:
        data.append(wins)

    for color in CardType:
        cardss = print_player_cards_by_color(player, color, "")
        if len(cardss) > 1:
            data.append(cardss)

    # print(tabulate(data))