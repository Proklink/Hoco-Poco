from abc import ABC, abstractmethod
from Graphics.settings import *
from pygame import Rect, Surface, font
import time
from cards import cards_by_colors
from InternalEvents import dispatch_event
from Graphics.settings import SPACE_BEETWEN_CARDS as INDENT



class GObject:
    def __init__(self):
        self.FONT = font.SysFont(None, 30)
    def expired(self):
        return False, []
    
    def blitme(self, screen):
        pass

    def click(self):
        pass

    def clickable(self):
        return False
    
def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

class NotificationExpired(GObject):
    '''
    args [text, expiration_time = 20000, generates = [], event = ""]
    '''
    WIDTH = 366
    HEIGHT = 300
    def __init__(self, args: list):
        super().__init__()
        self.text = str(args[0])
        self.expiration_time = time.time() + args[1]
        self.generates = args[2]
        self.event = args[3]

        self.image = Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(pygame.Color('grey'))
        self.rect = self.image.get_rect()
        self.rect.left = 1550
        self.rect.top = 540

        self.text_surface = Surface((self.WIDTH - 2*INDENT, self.HEIGHT - 2*INDENT))
        self.text_surface.fill(pygame.Color('grey'))

        blit_text(self.text_surface, self.text, (0,0), self.FONT)

        self.image.blit(self.text_surface, (INDENT, INDENT))

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
    WIDTH = 366
    HEIGHT = 300
    def __init__(self, args: list):
        super().__init__()
        self.text = str(args[0])
        self.generates = args[1]
        self.event = args[2]

        self.image = Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(pygame.Color('grey'))
        self.rect = self.image.get_rect()
        self.rect.left = 1550
        self.rect.top = 540

        self.text_surface = Surface((self.WIDTH - 2*INDENT, self.HEIGHT - 2*INDENT))
        self.text_surface.fill(pygame.Color('grey'))

        blit_text(self.text_surface, self.text, (0,0), self.FONT)

        self.image.blit(self.text_surface, (INDENT, INDENT))

    def blitme(self, screen):
        screen.screen.blit(self.image, self.rect)
        pass

class Button(GObject):
    WIDTH = 188
    HEIGHT = 75
    def __init__(self, text):
        super().__init__()
        self.text = text

        self.image = Surface((self.WIDTH, self.HEIGHT))
        # self.image.fill((0 ,255, 0))
        self.rect = self.image.get_rect()

        self.text_image = self.FONT.render(text, True, TEXT_COLOR, (0,0,0))
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.left = self.rect.width / 2 - self.text_image_rect.width / 2
        self.text_image_rect.top = self.rect.height / 2 - self.text_image_rect.height / 2
        self.image.blit(self.text_image, self.text_image_rect)

    def blitme(self, screen):
        screen.screen.blit(self.image, self.rect)

    def click(self):
        print('{} button clicked'.format(self.text))

def get_dialog(text):
    notification_surface = Notification([text, [], ''])
    button_yes = Button('Yes')
    button_no = Button('No')
    button_yes.rect.left = notification_surface.rect.left
    button_yes.rect.top = notification_surface.rect.bottom
    button_no.rect.right = notification_surface.rect.right
    button_no.rect.top = notification_surface.rect.bottom

    return [notification_surface, button_yes, button_no]

def get_railway_check_dialog():
    notification_surface = Notification(['Сколько кубиков бросаете?', [], ''])
    button_yes = Button('2')
    button_no = Button('1')
    button_yes.rect.left = notification_surface.rect.left
    button_yes.rect.top = notification_surface.rect.bottom
    button_no.rect.right = notification_surface.rect.right
    button_no.rect.top = notification_surface.rect.bottom

    button_yes.click = lambda: dispatch_event("dialog_answer", 'dice_number', 2)
    button_no.click = lambda: dispatch_event("dialog_answer", 'dice_number', 1)

    return [notification_surface, button_yes, button_no]

def get_radiotower_check_dialog():
    notification_surface = Notification(['Перебрасываете?', [], ''])
    button_yes = Button('Да')
    button_no = Button('Нет')
    button_yes.rect.left = notification_surface.rect.left
    button_yes.rect.top = notification_surface.rect.bottom
    button_no.rect.right = notification_surface.rect.right
    button_no.rect.top = notification_surface.rect.bottom

    button_yes.click = lambda: dispatch_event("dialog_answer", 'radiotower', True)
    button_no.click = lambda: dispatch_event("dialog_answer", 'radiotower', False)

    return [notification_surface, button_yes, button_no]


def get_graphic_info_player_self():
    notification_surface = Notification(['Нажмите на игрока, у которого хотите взять 5 монет или отмену', [], ''])
    button = Button('Отмена')

    button.rect.right = notification_surface.rect.right
    button.rect.top = notification_surface.rect.bottom

    button.click = lambda: dispatch_event("dialog_answer", 'cancel_telecenter', ())

    return [notification_surface, button]

def get_graphic_info_player_other(player_name):
    notification_surface = Notification(['Выбран игрок {}'.format(player_name), [], ''])
    button_cancel = Button('Отмена')
    button_apply = Button('ОК')

    button_cancel.rect.right = notification_surface.rect.right
    button_cancel.rect.top = notification_surface.rect.bottom
    button_apply.rect.left = notification_surface.rect.left
    button_apply.rect.top = notification_surface.rect.bottom

    button_cancel.click = lambda: dispatch_event("dialog_answer", 'cancel_telecenter', ())
    button_apply.click = lambda: dispatch_event("dialog_answer", 'apply_telecenter', ())

    return [notification_surface, button_cancel, button_apply]

    
def get_active_player_gobj(text):
    notif = Notification([text, [], ""])
    notif.rect.left = 0
    notif.rect.top = 0
    return notif

def get_current_dice_gobj(text):
    notif = Notification([text, [], ""])
    notif.rect.left = CARD_WIDTH * Notification.WIDTH + SPACE_BEETWEN_CARDS * (Notification.WIDTH - 1)
    notif.rect.top = 0
    return notif

def get_shop_button():
    button = Button('Магазин')
    button.rect.right = SCREEN_WIDTH - INDENT
    button.rect.top = INDENT

    button.click = lambda: dispatch_event("shop")
    return button

def get_graphic_info_shop():
    notification_surface = Notification(['Выберите в магазине карту, которую хотите купить или отмену', [], ''])
    button = Button('Отмена')

    button.rect.right = notification_surface.rect.right
    button.rect.top = notification_surface.rect.bottom

    button.click = lambda: dispatch_event("dialog_answer", 'cancel_shop', ())

    return [notification_surface, button]

def get_graphic_info_card(color, card_id):
    notification_surface = Notification(['Выбрана карта {}'.format(cards_by_colors[color.value][card_id].name), [], ''])
    button_cancel = Button('Отмена')
    button_apply = Button('ОК')
    button_cancel.rect.right = notification_surface.rect.right
    button_cancel.rect.top = notification_surface.rect.bottom
    button_apply.rect.left = notification_surface.rect.left
    button_apply.rect.top = notification_surface.rect.bottom
    button_cancel.click = lambda: dispatch_event("dialog_answer", 'cancel_shop', ())
    button_apply.click = lambda: dispatch_event("dialog_answer", 'apply_shop', ())
    return [notification_surface, button_apply, button_cancel]