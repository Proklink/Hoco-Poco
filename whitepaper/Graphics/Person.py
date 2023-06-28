from pygame import Surface
from cards import CardType, cards_by_colors
from Graphics.settings import *
from Graphics.settings import SPACE_BEETWEN_CARDS as IND
from InternalEvents import dispatch_event, set_handler
from Graphics.GInfo import *

class CardBoard(GObject):
    coordinates = {
        CardType.BLUE : [
             (IND, IND),
             (2*IND + CARD_WIDTH, IND),
             (3*IND + 2*CARD_WIDTH, IND),
             (4*IND + 3*CARD_WIDTH, IND),
             (5*IND + 4*CARD_WIDTH, IND)
        ],
        CardType.GREEN : [
             (IND, 2*IND + CARD_HEIGHT),
             (2*IND + CARD_WIDTH, 2*IND + CARD_HEIGHT),
             (3*IND + 2*CARD_WIDTH, 2*IND + CARD_HEIGHT),
             (4*IND + 3*CARD_WIDTH, 2*IND + CARD_HEIGHT),
             (5*IND + 4*CARD_WIDTH, 2*IND + CARD_HEIGHT)
        ],
        CardType.RED : [
             (IND, 3*IND + 2*CARD_HEIGHT),
             (2*IND + CARD_WIDTH, 3*IND + 2*CARD_HEIGHT)
        ],
        CardType.PURPLE : [
             (3*IND + 2*CARD_WIDTH, 3*IND + 2*CARD_HEIGHT),
             (4*IND + 3*CARD_WIDTH, 3*IND + 2*CARD_HEIGHT),
             (5*IND + 4*CARD_WIDTH, 3*IND + 2*CARD_HEIGHT)
        ],
        CardType.WIN : [
             (8*IND + 5*CARD_WIDTH, IND),
             (9*IND + 6*CARD_WIDTH, IND),
             (8*IND + 5*CARD_WIDTH, 2*IND + CARD_HEIGHT),
             (9*IND + 6*CARD_WIDTH, 2*IND + CARD_HEIGHT)
        ]
    }

    WIDTH = 975
    HEIGHT = 500
    def __init__(self):
        self.board = Surface((self.WIDTH, self.HEIGHT))
        self.rect = self.board.get_rect()
        self.rect.left = 252#x
        self.rect.top = 540#y
        self.cards = [{},{},{},{},{}]


    def added(self, card_id, color: CardType):
        image = cards_by_colors[color.value][card_id].gui_settings.image.copy()
        rect = image.get_rect()
        rect.left = self.coordinates[color][card_id][0]
        rect.top = self.coordinates[color][card_id][1]
        self.cards[color.value][card_id] = (image, rect)
        self.update()

    def deleted(self, card_id, color: CardType):
        self.cards[color.value][card_id] = ()
        self.update()

    def update(self):
        self.board.fill(0xD9D9D9)
        for color in CardType:
            for card_id in self.cards[color.value]:
                if self.cards[color.value][card_id] != ():
                    self.board.blit(self.cards[color.value][card_id][0], self.cards[color.value][card_id][1])
    
    def blitme(self, screen):
        screen.screen.blit(self.board, self.rect)

    def click(self, x, y):
        x -= self.rect.left
        y -= self.rect.top
        for color in CardType:
            for card_id in self.cards[color.value]:
                if self.cards[color.value][card_id] == ():
                    continue

                if self.cards[color.value][card_id][1].collidepoint(x, y):
                    dispatch_event('card', color, card_id)


class MiniCardBoard(GObject):
    coordinates = {
        CardType.BLUE : [
             (IND, IND),
             (IND, 2*IND + CARD_MINI_HEIGHT),
             (IND, 3*IND + 2*CARD_MINI_HEIGHT),
             (IND, 4*IND + 3*CARD_MINI_HEIGHT),
             (IND, 5*IND + 4*CARD_MINI_HEIGHT)
        ],
        CardType.GREEN : [
             (2*IND + CARD_MINI_WIDTH, IND),
             (2*IND + CARD_MINI_WIDTH, 2*IND + CARD_MINI_HEIGHT),
             (2*IND + CARD_MINI_WIDTH, 3*IND + 2*CARD_MINI_HEIGHT),
             (2*IND + CARD_MINI_WIDTH, 4*IND + 3*CARD_MINI_HEIGHT),
             (2*IND + CARD_MINI_WIDTH, 5*IND + 4*CARD_MINI_HEIGHT)
        ],
        CardType.RED : [
             (3*IND + 2*CARD_MINI_WIDTH, IND),
             (3*IND + 2*CARD_MINI_WIDTH, 2*IND + CARD_MINI_HEIGHT)
        ],
        CardType.PURPLE : [
             (3*IND + 2*CARD_MINI_WIDTH, 3*IND + 2*CARD_MINI_HEIGHT),
             (3*IND + 2*CARD_MINI_WIDTH, 4*IND + 3*CARD_MINI_HEIGHT),
             (3*IND + 2*CARD_MINI_WIDTH, 5*IND + 4*CARD_MINI_HEIGHT)
        ],
        CardType.WIN : [
             (IND,                       6*IND + 6*CARD_MINI_HEIGHT),
             (2*IND + CARD_MINI_WIDTH,   6*IND + 6*CARD_MINI_HEIGHT),
             (3*IND + 2*CARD_MINI_WIDTH, 6*IND + 6*CARD_MINI_HEIGHT),
             (4*IND + 3*CARD_MINI_WIDTH, 6*IND + 6*CARD_MINI_HEIGHT)
        ]
    }

    WIDTH = 465
    HEIGHT = 500
    playres_boards = {
        0 : (15, 26),
        1 : (15 + WIDTH + IND, 26),
        2 : (15 + 2*WIDTH + 2*IND, 26)
    }

    def __init__(self, id):
        self.board = Surface((self.WIDTH, self.HEIGHT))
        self.rect = self.board.get_rect()
        self.rect.left = self.playres_boards[id][0]
        self.rect.top = self.playres_boards[id][1]
        self.cards = [[], [], [], [], []]

    def added(self, card_id, color: CardType):
        self.cards[color.value].append(card_id)
        self.update()

    def deleted(self, card_id, color: CardType):
        del self.cards[color.value][card_id]
        self.update()

    def update(self):
        self.board.fill(0xD9D9D9)
        for color in CardType:
            for card_id in self.cards[color.value]:
                image = cards_by_colors[color.value][card_id].gui_settings.image_mini.copy()
                self.board.blit(image, (self.coordinates[color][card_id][0], self.coordinates[color][card_id][1]))

    def blitme(self, screen):
        screen.screen.blit(self.board, self.rect)

    def click(self):
        pass


class ActivePlayer(GObject):
    def __init__(self, player):
        self.player = player
        self.pl_changed = False
        set_handler('player'+str(self.player.id), self.player_changed)

        self.main_card_board = CardBoard(252, 540)
        self.main_card_board.update(self.player.cards)

    def player_changed(self):
        self.pl_changed = True

    def update(self):
        if self.pl_changed:
            self.main_card_board.update(self.player.cards)
            self.pl_changed = False

    def blitme(self, screen):
        screen.screen.blit(self.main_card_board.board, self.main_card_board.rect)


class OtherPlayer(GObject):
    def __init__(self, player):
        self.player = player
        self.pl_changed = False
        set_handler('player'+str(self.player.id), self.player_changed)

        self.main_card_board = MiniCardBoard(15, 26)
        self.main_card_board.update(self.player.cards)

    def player_changed(self):
        self.pl_changed = True

    def update(self):
        if self.pl_changed:
            self.main_card_board.update(self.player.cards)
            self.pl_changed = False

    def blitme(self, screen):
        screen.screen.blit(self.main_card_board.board, self.main_card_board.rect)

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

class BigCard(GObject):
    WIDTH = 300
    HEIGHT = 500
    def __init__(self):
        set_handler('card', self.update)
        self.board = Surface((self.WIDTH, self.HEIGHT))
        self.rect = self.board.get_rect()
        self.rect.left = 1240
        self.rect.top = 540
        self.FONT = font.SysFont(None, 30)
        

    def update(self, color, card_id):
        self.board.fill(pygame.Color('grey'))
        card = cards_by_colors[color.value][card_id]
        
        header_str = card.name
        if color.value != CardType.WIN.value:
            dice_str = " {}".format(card.dice)
            header_str += dice_str

        header_text_image = self.FONT.render(header_str, True, TEXT_COLOR, pygame.Color('grey'))
        header_text_rect = header_text_image.get_rect()
        header_text_rect.left = 22
        header_text_rect.top = 4
        
        card_image = cards_by_colors[color.value][card_id].gui_settings.image_big.copy()
        card_rect = card_image.get_rect()
        card_rect.left = 22
        card_rect.top = 4 + header_text_rect.bottom

        main_text_surface = Surface((256, self.HEIGHT - card_rect.height - header_text_rect.height - 8))
        main_text_surface.fill(pygame.Color('grey'))
        main_text = "Стоит: {}\n{}".format(card.cost, card.descr)

        blit_text(main_text_surface, main_text, (0,0), self.FONT)

        self.board.blit(header_text_image, header_text_rect)
        self.board.blit(card_image, card_rect)
        self.board.blit(main_text_surface, (22, 4 + card_rect.bottom))

    
    def blitme(self, screen):
        screen.screen.blit(self.board, self.rect)

    def click(self, x, y):
        pass


class ActionInfo(GObject):
    WIDTH = 366
    HEIGHT = 300
    def __init__(self):
        super().__init__()
        set_handler('action_text', self.set_action_text)
        self.FONT = font.SysFont(None, 30)
        self.text = ""

        self.image = Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(pygame.Color('grey'))
        self.rect = self.image.get_rect()
        self.rect.left = 1550
        self.rect.top = 540

        self.text_surface = Surface((self.WIDTH - 2*INDENT, self.HEIGHT - 2*INDENT))
        self.text_surface.fill(pygame.Color('grey'))

        self.set_action_text(self.text)

        self.image.blit(self.text_surface, (INDENT, INDENT))

    def set_action_text(self, text):
        self.text = text
        blit_text(self.text_surface, self.text, (0,0), self.FONT)


    def blitme(self, screen):
        screen.screen.blit(self.image, self.rect)
        pass