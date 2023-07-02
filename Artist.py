import pygame
from Graphics.settings import *
from Graphics.GInfo import *
from Graphics.Person import *
from InternalEvents import dispatch_event, set_handler

#players_coordinates
plrs_crds = {
    0 : {
        'left' : 15,
        'right' : 480,
        'top' : 26,
        'bottom' : 526
    },
    1 : {
        'left' : 484,
        'right' : 949,
        'top' : 26,
        'bottom' : 526
    },
    2 : {
        'left' : 953,
        'right' : 1418,
        'top' : 26,
        'bottom' : 526
    }
}

#big_board_coordinates
bbrd_crds = {
    'left' : 252,
    'right' : 1227,
    'top' : 540,
    'bottom' : 1040
}

class Artist():
    def __init__(self, screen, settings, players, clock, shop):
        self.players = players
        self.settings = settings
        self.window = screen
        self.clock = clock
        self.fps = FPS(self.clock)
        self.clear_color = (0, 0, 0)
        self.graphic_objects = [GObject(), self.fps]
        self.dialog_objects = []
        
        self.last_clicked_player = -1
        self.last_clicked_card = ()

        set_handler("new_grafics", self.new_grafics)
        set_handler("new_dialog", self.new_dialog)
        set_handler("click", self.click)
        set_handler("dialog_answer", self.dialog_answer)
        set_handler("active_player", self.new_active_player)
        set_handler('dice', self.new_dice)
        set_handler('shop', self.display_shop)

        self.shop_button = get_shop_button()
        self.shop = shop

        self.graphic_objects.append(players[0].mini_board)
        self.graphic_objects.append(players[1].mini_board)
        self.graphic_objects.append(BigCard())
        self.graphic_objects.append(self.shop_button)


    def display_shop(self):
        self.graphic_objects[0] = self.shop.big_card_board

    def card_clicked(self, color, card_id):
        self.last_clicked_card = (color, card_id)

    def new_dice(self, dice):
        dice_str = ''
        if len(dice) == 1:
            dice_str = str(dice[0])
        else:
            dice_str = '{} - {}'.format(dice[1], dice[2])
        self.current_dice_static_notification = get_current_dice_gobj(dice_str)

    def new_active_player(self, player):
        self.active_player_static_notification = get_active_player_gobj('Ход игрока {}'.format(player.name))

    def standart_click(self, m_x, m_y):
        for dialogs in self.dialog_objects:
            for button in dialogs:
                if button.rect.collidepoint(m_x, m_y):
                    button.click()
        if self.shop_button.rect.collidepoint(m_x, m_y):
            self.shop_button.click()

        for i in range(len(self.players)):
            if m_x >= plrs_crds[i]['left']  and \
               m_x <= plrs_crds[i]['right'] and \
               m_y >= plrs_crds[i]['top']   and \
               m_y <= plrs_crds[i]['bottom']:
                self.graphic_objects[0] = self.players[i].big_card_board
                self.last_clicked_player = i
                dispatch_event('player_clicked', i)
        
        if m_x >= bbrd_crds['left']  and \
           m_x <= bbrd_crds['right'] and \
           m_y >= bbrd_crds['top']   and \
           m_y <= bbrd_crds['bottom']:
            self.graphic_objects[0].click(m_x, m_y)
        
    
    def click(self, m_x, m_y):
        print(m_x, " ", m_y)
        self.standart_click(m_x, m_y)
    
    def clear_dialogs(self):
        for dialogs in self.dialog_objects:
            for dialog_gobject in dialogs:
                self.graphic_objects.remove(dialog_gobject)
            dispatch_event('update_continuation')
        self.dialog_objects = []

    def dialog_answer(self, next_event, answer):
        if next_event != '':
            dispatch_event(next_event, answer)
        
        self.clear_dialogs()

    def new_dialog(self, new_gobjects):
        self.clear_dialogs()
        self.dialog_objects.append(new_gobjects)
        for gobject in new_gobjects:
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

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for gbj in self.graphic_objects:
            if gbj.clickable():
                if gbj.rect.collidepoint(mouse_x, mouse_y):
                    gbj.is_border = True
                else:
                    gbj.is_border = False
        self.graphic_objects[0].hover(mouse_x, mouse_y)

        self.fps.update()

    def draw(self):
        self.window.screen.fill(self.clear_color)
        self.window.screen.blit(self.window.image, self.window.rect)

        for gobject in self.graphic_objects:
            gobject.blitme(self.window)

        pygame.display.flip()