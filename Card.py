import pygame

class Card(pygame.sprite.Sprite):
    purchased = 0

    def __init__(self, card):
        super().__init__()
        self.max = card["max"]

        if Card.purchased >= self.max:
            raise "there are no more cards"
        else:
            Card.purchased += 1

        
        self.image = pygame.Surface((50, 100))
        self.rect = self.image.get_rect()
        self.name = card["name"]
        self.cost = card["cost"]
        self.profit = card["profit"]
        self.trigger = card["trigger"]
        self.priority = card["priority"]
        self.color = card["color"]
        self.description = card["description"]

    def update(self, *args):
        x = args[0]
        y = args[1]
        self.rect.x = x
        self.rect.y = y
        self.image.fill(self.color)
        
