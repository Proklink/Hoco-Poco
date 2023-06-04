from pygame import Surface
import pygame.font
from pygame.transform import smoothscale
from settings import CARD_MINI_HEIGHT, CARD_MINI_WIDTH
from cards import win_cards

class GUIPlayer:
    def __init__(self, player, screen, settings):
        self.player = player
        self.screen = screen
        self.settings = settings

        TEXT_COLOR = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 30)

        self.coin_image = settings.coin_image.copy()
        self.coin_image = smoothscale(self.coin_image, (50, 50))
        self.coin_rect = self.coin_image.get_rect()

        self.money_str = '10'
        self.money_image = self.font.render(self.money_str, True, TEXT_COLOR, (255, 255, 255))
        # self.money_image = smoothscale(self.money_image, (50, 50))
        self.money_rect = self.money_image.get_rect()


        self.money_surface = Surface((self.coin_rect.width + 10 + self.money_rect.width, self.coin_rect.height))

        self.money_surface.blit(self.coin_image, (0, 0))
        self.money_surface.blit(self.money_image, (self.coin_rect.right + 5, 0))

        self.player_name_image = self.font.render('Player 1', True, TEXT_COLOR, (255, 255, 255))
        self.player_image =  settings.car_image
        self.player_image = smoothscale(self.player_image, (100, 100))
        height = self.player_image.get_rect().height + self.player_name_image.get_rect().height
        self.player_surface = Surface((100, height))
        self.player_surface.fill((255, 255, 255))
        self.player_surface.blit(self.player_name_image, (0, 0))
        self.player_surface.blit(self.player_image, (0, self.player_name_image.get_rect().height))

        self.win_cards = [0, 1, 2]#надо получать из self.player
        real_height = (CARD_MINI_HEIGHT) * len(self.win_cards)
        real_width = CARD_MINI_WIDTH
        self.win_card_board = Surface((real_width, real_height))
        accumulated_y = 0
        for card_id in self.win_cards:
            image = smoothscale(win_cards[card_id].gui_settings.image, (CARD_MINI_WIDTH, CARD_MINI_HEIGHT))
            self.win_card_board.blit(image, (0, accumulated_y))
            accumulated_y += CARD_MINI_HEIGHT

        self.player_background = Surface((300, 300))
        self.player_background.fill((255, 255, 255))

        self.player_background.blit(self.money_surface, (0, 0))
        self.player_background.blit(self.player_surface, (self.money_surface.get_rect().right + 10, 0))
        self.player_background.blit(self.win_card_board, (self.money_surface.get_rect().right + 10 + self.player_surface.get_rect().right + 10, 0))
        self.player_background_rect = self.player_background.get_rect()
        self.player_background_rect.left = 500
        self.player_background_rect.top = 0

    def update(self, bullets):
        """Update the ship's position based on the movement flag."""
        
        pass

    def blitme(self):
        """Draw the ship at its current location."""

        self.screen.screen.blit(self.player_background, self.player_background_rect)



