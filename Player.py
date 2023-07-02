from cards import CardType
import cards as card_file
from InternalEvents import dispatch_event
from Graphics.Person import *

class Player:
    __player_numbers = 0
    def __init__(self, name):
        self.money = 0
        self.name = name
        self.id = Player.__player_numbers
        self.cards = [{}, {}, {}, {}, {}]
        Player.__player_numbers += 1
        self.mini_board = MiniCardBoard(self.id, self.name)
        self.big_card_board = CardBoard()

    def add_money(self, money):
        self.money += money
        self.mini_board.money(self.money)

    def del_money(self, money):
        self.money -= money
        self.mini_board.money(self.money)

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
        self.mini_board.added(card_id, color, colored_cards[card_id])
        self.big_card_board.added(card_id, color, colored_cards[card_id])


    def del_card(self, card_id, color: CardType, unsubscribe):
        colored_cards = self.cards[color.value]
        number = colored_cards.get(card_id)
        if number != None:
            if colored_cards[card_id] > 1:
                colored_cards[card_id] -= 1

                self.mini_board.deleted(card_id, color, colored_cards[card_id])
                self.big_card_board.deleted(card_id, color, colored_cards[card_id])
            else:
                del colored_cards[card_id]
                
                self.mini_board.deleted(card_id, color, None)
                self.big_card_board.deleted(card_id, color, None)
        if color.value != CardType.WIN.value:
            card = card_file.cards_by_colors[color.value][card_id]
            unsubscribe(card.dice, card, self.id, color)
        


