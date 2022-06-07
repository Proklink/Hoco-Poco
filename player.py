import cards, random, pygame
from common import DISPLAY_WIDTH, DISPLAY_HEIGHT, CARD_HEIGHT, CARD_WIDTH
from Card import Card

class Player:
    def __init__(self):
        self.money = 3
        self.cards = [Card(cards.FARM), Card(cards.WHEAT)]

    def update(self, *args):
        screen = args[0]
        for i in range(len(self.cards)):
            self.cards[i].update(10 + i * (CARD_WIDTH + 10), DISPLAY_HEIGHT - CARD_HEIGHT)
            screen.blit(self.cards[i].image, self.cards[i].rect)

    @staticmethod
    def dice_roll(roll_num):
        if roll_num == 1:
            return random.randint(1, 6)
        else:
            return [random.randint(1, 6), random.randint(1, 6)]
            