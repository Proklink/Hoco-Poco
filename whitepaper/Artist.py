import pygame
from Graphics.settings import *
from Graphics.GInfo import get_dialog


class Artist():
    def __init__(self, screen, settings):
        self.settings = settings
        self.window = screen
        self.clear_color = (0, 0, 0)
        self.grapfic_objects = []

    def update(self, new_gobjects):
        for gobject in self.grapfic_objects:
            ret, generated = gobject.expired()
            if not ret:
                continue
            self.grapfic_objects.remove(gobject)
            new_gobjects += generated

        for new_gobj in new_gobjects:
            self.grapfic_objects.append(new_gobj[0](new_gobj[1]))

    def draw(self):
        self.window.screen.fill(self.clear_color)
        self.window.screen.blit(self.window.image, self.window.rect)

        for gobject in self.grapfic_objects:
            gobject.blitme(self.window)

        pygame.display.flip()