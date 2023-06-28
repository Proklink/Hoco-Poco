from cards import CardType
import cards as card_file
from InternalEvents import dispatch_event
from Graphics.Person import *

class Player:
    __player_numbers = 0
    def __init__(self, name):
        self.money = 3
        self.name = name
        self.id = Player.__player_numbers
        self.cards = [{}, {}, {}, {}, {}]
        Player.__player_numbers += 1
        # self.event_str = 'player'+str(self.id)
        self.mini_board = MiniCardBoard(self.id)
        self.big_card_board = CardBoard()


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
        self.mini_board.added(card_id, color)
        self.big_card_board.added(card_id, color)
        # dispatch_event(self.event_str)

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
        self.mini_board.added(card_id, color)
        self.big_card_board.added(card_id, color)
        # dispatch_event(self.event_str)

