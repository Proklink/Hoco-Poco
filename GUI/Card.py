from pygame.transform import smoothscale

from pygame.sprite import Sprite
from pygame.color import THECOLORS
import pygame

class Card(Sprite):

    def __init__(self, screen, image, posx, posy):
        """Initialize the ship and set its starting position."""
        
        super(Card, self).__init__()

        self.screen = screen
        
        # Load the ship image and get its rect.
        self.image = image.copy()
        self.rect = self.image.get_rect()
        # self.image = smoothscale(self.image, (self.rect.width, self.rect.height))
        self.rect = self.image.get_rect()
        self.rect.top = posy
        self.rect.left = posx
        print(self.rect.width, " ", self.rect.height)
        
    def update(self, bullets):
        """Update the ship's position based on the movement flag."""
        
        pass

    def blitme(self):
        """Draw the ship at its current location."""

        self.screen.screen.blit(self.image, self.rect)