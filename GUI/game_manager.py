import sys, pygame
from Card import Card
from game_stat import GameStats
import game_events as ge
from pygame.color import THECOLORS
from CardBoard import CardBoard
from GUIPlayer import GUIPlayer


class Manager():
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.stats = GameStats(self.settings)      
        self.init_game()

    def init_game(self):
        # self.car = Card(self.screen, self.settings.ferma_image, 500, 500)

        self.cards = [  [ 0, 1],
                        [0, 1, 2, 3, 4],
                        [0, 1, 2, 3, 4],
                        [0, 1, 2],
                        [0, 1, 2, 3]
        ]
        self.cb = CardBoard(self.screen, self.cards)
        self.stats.reset_stats()
        self.player1 = GUIPlayer(1, self.screen, self.settings)

    def events(self):
        if self.stats.game_active:
            ge.check_events_game_active(self, self.cb, self.stats)
        else:
            ge.check_events_game_inactive(self, self.stats)
    
    def update(self):
        pass
        # if self.stats.game_active:
        #     self.ship.update(None)

    def draw(self):
        if self.stats.game_active:
            self.draw_game_screen()
        else:
            self.draw_menu_screen()
        pygame.display.flip()


    def draw_game_screen(self):
        """Update images on the screen and flip to the new screen."""

        self.screen.screen.blit(self.screen.image, self.screen.rect)
        self.cb.blitme()
        # self.car.blitme()
        # self.player1.blitme()

    def draw_menu_screen(self):
        self.screen.screen.blit(self.screen.image, self.screen.rect)
        pygame.draw.rect(self.screen.screen, THECOLORS['black'], self.screen.rect)