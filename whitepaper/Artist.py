import pygame
from Graphics.settings import *
from Graphics.GInfo import *
from InternalEvents import dispatch_event, set_handler

class Artist():
    def __init__(self, screen, settings):
        self.settings = settings
        self.window = screen
        self.clear_color = (0, 0, 0)
        self.graphic_objects = []
        self.dialog_objects = []

        set_handler("new_grafics", self.new_grafics)
        set_handler("new_dialog", self.new_dialog)
        set_handler("click", self.click)
        set_handler("dialog_answer", self.dialog_answer)

    def click(self, m_x, m_y):
        for button in self.dialog_objects:
            if button.rect.collidepoint(m_x, m_y):
                button.click()

    def dialog_answer(self, next_event, answer):
        dispatch_event(next_event, answer)
        
        for dialog_gobject in self.dialog_objects:
            self.graphic_objects.remove(dialog_gobject)
        self.dialog_objects = []
        dispatch_event('update_continuation')

    def new_dialog(self, new_gobjects):
        for gobject in new_gobjects:
            self.dialog_objects.append(gobject)
            self.graphic_objects.append(gobject)

    def new_grafics(self, new_gobjects):
        for new_gobj in new_gobjects:
                self.graphic_objects.append(new_gobj[0](new_gobj[1]))

    def update(self):
        new_gobjects = []
        for gobject in self.graphic_objects:
            ret, generated = gobject.expired()
            if not ret:
                continue
            self.graphic_objects.remove(gobject)
            new_gobjects += generated

        for new_gobj in new_gobjects:
            self.graphic_objects.append(new_gobj[0](new_gobj[1]))

    def draw(self):
        self.window.screen.fill(self.clear_color)
        self.window.screen.blit(self.window.image, self.window.rect)

        for gobject in self.graphic_objects:
            gobject.blitme(self.window)

        pygame.display.flip()