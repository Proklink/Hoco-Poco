from abc import ABC, abstractmethod
from Graphics.settings import CARD_HEIGHT, CARD_WIDTH, SPACE_BEETWEN_CARDS
from pygame import Rect, Surface, font
import time
from InternalEvents import dispatch_event

class GObject:
    def expired(self):
        return False, []
    
    def blitme(self, screen):
        pass

    def click(self):
        pass

class GBase(GObject):
    def __init__(self, left, top):
        self.width = CARD_WIDTH
        self.height = CARD_HEIGHT
        self.left = left
        self.top = top

        self.clickable_object = None
        self.renderable_object = None

        self.image = Surface((self.width, self.height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.top = self.top
        self.rect.left = self.left

    def set_click(self, click_handler):
        self.click_handler = click_handler

    def set_render(self, renderable):
        self.renderable_object = renderable

    def blitme(self, screen):
        screen.screen.blit(self.image, self.rect)
        if self.renderable_object is not None:
            self.renderable_object.blitme(screen)

    def click(self):
        if self.clickable_object is not None:
            self.click_handler()

class Notification(GObject):
    '''
    args [text, expiration_time = 20000, generates = [], event = ""]
    '''
    WIDTH = 4
    HEIGHT = 1
    x = 5
    y = 3
    def __init__(self, args: list):
        super().__init__()
        self.text = str(args[0])
        self.expiration_time = time.time() + args[1]
        self.generates = args[2]
        self.event = args[3]

        image_width = CARD_WIDTH * self.WIDTH + SPACE_BEETWEN_CARDS * (self.WIDTH - 1)

        self.image = Surface((image_width, CARD_HEIGHT))
        self.text_color = (69, 69, 69)
        self.font = font.SysFont(None, 50)
        self.text_image = self.font.render(self.text, True, self.text_color, (0,0,0))
        self.text_image_rect = self.text_image.get_rect()

        self.image.blit(self.text_image, (0, 0))
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.left = x
        self.rect.top = y

    def expired(self):
        now = time.time()

        if self.expiration_time <= now:
            if self.event != "":
                dispatch_event(self.event)
            return True, self.generates
        
        return False, []

    def blitme(self, screen):
        screen.screen.blit(self.image, self.rect)


def get_button(self, text):
    image = Surface((CARD_WIDTH, CARD_HEIGHT))

    msg_image = self.font.render(text, True, self.text_color, (0,0,0))
    msg_image_rect = msg_image.get_rect()
    image.blit(msg_image, msg_image_rect)
    return image

class Dialog(GObject):
    '''
    args [text, generates = [], event = ""]
    '''
    WIDTH = 4
    HEIGHT = 1
    x = 5
    y = 3
    def __init__(self, args: list):
        super().__init__()
        self.text = str(args[0])
        # self.expiration_time = time.time() + args[1]
        self.generates = args[1]
        self.event = args[2]

        self.image = Surface((CARD_WIDTH * 3, CARD_HEIGHT * 2))
        self.text_color = (69, 69, 69)
        self.font = font.SysFont(None, 50)
        self.text_image = self.font.render(self.text, True, self.text_color, (0,0,0))
        # self.text_image_rect = self.text_image.get_rect()

        self.button_yes = get_button('Да')
        self.button_yes_rect = self.button_yes.get_rect()
        self.button_yes_rect.top = CARD_HEIGHT
        self.button_yes_rect.left = 500
        self.button_no = get_button('Нет')
        self.button_no_rect = self.button_no.get_rect()
        self.button_no_rect.top = 600
        self.button_no_rect.left = 600

        self.image.blit(self.text_image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.top = 500
        self.rect.left = 500


    def expired(self):
        now = time.time()

        if self.expiration_time <= now:
            if self.event != "":
                dispatch_event(self.event)
            return True, self.generates
        
        return False, []

    def blitme(self, screen):
        screen.screen.blit(self.image, self.rect)



    

