from abc import ABC, abstractmethod
from Graphics.settings import *
from pygame import Rect, Surface, font
import time
from InternalEvents import dispatch_event



class GObject:
    def __init__(self):
        self.FONT = font.SysFont(None, 50)
    def expired(self):
        return False, []
    
    def blitme(self, screen):
        pass

    def click(self):
        pass

    def clickable(self):
        return False

class NotificationExpired(GObject):
    '''
    args [text, expiration_time = 20000, generates = [], event = ""]
    '''
    WIDTH = 4
    HEIGHT = 1
    def __init__(self, args: list):
        super().__init__()
        self.text = str(args[0])
        self.expiration_time = time.time() + args[1]
        self.generates = args[2]
        self.event = args[3]

        image_width = CARD_WIDTH * self.WIDTH + SPACE_BEETWEN_CARDS * (self.WIDTH - 1)

        self.image = Surface((image_width, CARD_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left = SCREEN_WIDTH / 2 - self.rect.width / 2
        self.rect.top = SCREEN_HEIGHT / 2 - self.rect.height / 2

        self.text_image = self.FONT.render(self.text, True, TEXT_COLOR, (0,0,0))
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.left = self.rect.width / 2 - self.text_image_rect.width / 2
        self.text_image_rect.top = self.rect.height / 2 - self.text_image_rect.height / 2

        self.image.blit(self.text_image, self.text_image_rect)
        

    def expired(self):
        now = time.time()

        if self.expiration_time <= now:
            if self.event != "":
                dispatch_event(self.event)
            return True, self.generates
        
        return False, []

    def blitme(self, screen):
        screen.screen.blit(self.image, self.rect)
        pass
    
class Notification(GObject):
    '''
    args [text, generates = [], event = ""]
    '''
    WIDTH = 4
    HEIGHT = 1
    def __init__(self, args: list):
        super().__init__()
        self.text = str(args[0])
        self.generates = args[1]
        self.event = args[2]

        image_width = CARD_WIDTH * self.WIDTH + SPACE_BEETWEN_CARDS * (self.WIDTH - 1)

        self.image = Surface((image_width, CARD_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left = SCREEN_WIDTH / 2 - self.rect.width / 2
        self.rect.top = SCREEN_HEIGHT / 2 - self.rect.height / 2

        self.text_image = self.FONT.render(self.text, True, TEXT_COLOR, (0,0,0))
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.left = self.rect.width / 2 - self.text_image_rect.width / 2
        self.text_image_rect.top = self.rect.height / 2 - self.text_image_rect.height / 2

        self.image.blit(self.text_image, self.text_image_rect)

    def blitme(self, screen):
        screen.screen.blit(self.image, self.rect)
        pass

class Button(GObject):
    def __init__(self, text):
        super().__init__()
        self.text = text

        self.image = Surface((CARD_WIDTH / 2, CARD_HEIGHT / 2))
        self.image.fill((0 ,255, 0))
        self.rect = self.image.get_rect()

        self.text_image = self.FONT.render(text, True, TEXT_COLOR, (0,0,0))
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.left = self.rect.width / 2 - self.text_image_rect.width / 2
        self.text_image_rect.top = self.rect.height / 2 - self.text_image_rect.height / 2
        self.image.blit(self.text_image, self.text_image_rect)

    def blitme(self, screen):
        screen.screen.blit(self.image, self.rect)

    def click(self):
        print('{self.text} button clicked'.format(self.text))

    def clickable(self):
        return True


def get_dialog():
    notification_surface = Notification(['Хотите?', [], ''])
    button_yes = Button('Yes')
    button_no = Button('No')
    button_yes.rect.left = notification_surface.rect.left
    button_yes.rect.top = notification_surface.rect.bottom
    button_no.rect.right = notification_surface.rect.right
    button_no.rect.top = notification_surface.rect.bottom

    return [notification_surface, button_yes, button_no]


    

