import pygame


class Screen():
    def __init__(self, width, height, caption, image):
        self.width = width
        self.height = height
        self.caption = caption
        self.image = image.copy()
        self.rect = self.image.get_rect()
        self.screen = pygame.display.set_mode((self.width, self.height))