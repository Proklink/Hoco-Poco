import pygame
from GameEvents import GameIvents
from MainPipline import MainPipline
from Artist import Artist
from Graphics.screen import Screen
from Graphics.settings import Settings
from Player import Player
from Graphics.settings import MAX_FPS
from Graphics.GInfo import FPS
from Graphics.Person import Shop


class Manager():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.players = [Player("Player1"), Player("Player2"), Player("Player3")]
        self.settings = Settings()
        self.game_events = GameIvents()
        self.shop = Shop()
        self.main_pipline = MainPipline(self.players, self.shop)
        self.screen = Screen(self.settings.scr_width,
                             self.settings.scr_height,
                             self.settings.scr_caption,
                             self.settings.scr_image)
        self.artist = Artist(self.screen, self.settings, self.players, self.clock, self.shop)
        self.fps = FPS(self.clock)
    
    def events(self):
        self.game_events.run()
    
    def update(self):
        self.main_pipline.update()
        self.main_pipline.run()
        self.artist.update()

    def draw(self):
        self.artist.draw()
        self.clock.tick(MAX_FPS)