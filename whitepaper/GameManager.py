import pygame
from GameEvents import GameIvents
from MainPipline import MainPipline
from Artist import Artist
from Graphics.screen import Screen
from Graphics.settings import Settings



class Manager():
    def __init__(self):
        self.settings = Settings()
        self.game_events = GameIvents()
        self.main_pipline = MainPipline()
        self.screen = Screen(self.settings.scr_width,
                             self.settings.scr_height,
                             self.settings.scr_caption,
                             self.settings.scr_image)
        self.artist = Artist(self.screen, self.settings)

    
    def events(self):
        self.game_events.run()
    
    def update(self):
        self.main_pipline.update()
        new_graphic_objects = self.main_pipline.run()
        self.artist.update(new_graphic_objects)

    def draw(self):
        self.artist.draw()