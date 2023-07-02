from pygame import Surface
from cards import CardType, cards_by_colors
from Graphics.settings import *
from Graphics.settings import SPACE_BEETWEN_CARDS as IND
from InternalEvents import dispatch_event, set_handler
from Graphics.GInfo import *


class BigCard(GObject):
    WIDTH = BIG_CARD_WIDTH
    HEIGHT = BIG_CARD_HEIGHT
    RIGHT = SCREEN_WIDTH - 2*IND - NOTIFICATION_WIDTH
    TOP = BIG_CARD_TOP
    def __init__(self):
        super().__init__()
        set_handler('card', self.update)
        self.board = Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.rect = self.board.get_rect()
        self.rect.right = self.RIGHT
        self.rect.top = self.TOP        

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

    WIDTH = CARD_BOARD_WIDTH
    HEIGHT = CARD_BOARD_HEIGHT
    RIGHT = BigCard.RIGHT - BIG_CARD_WIDTH - IND
    def __init__(self):
        super().__init__()
        self.board = Surface((self.WIDTH, self.HEIGHT))
        self.rect = self.board.get_rect()
        self.rect.right = self.RIGHT                   #x
        self.rect.bottom = SCREEN_HEIGHT - IND #y
        self.cards = [{},{},{},{},{}]

        self.card_border_rect = Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)

    def get_multyplyer(self, number, card_rect):
        surface = Surface((16, 16), pygame.SRCALPHA)
        rect = surface.get_rect()
        rect.right = card_rect.right
        rect.top = card_rect.top
        blit_text(surface, str(number), (0,0), self.FONT)
        return surface, rect

    def added(self, card_id, color: CardType, number):
        if self.cards[color.value].get(card_id) != None:
            mtuple = self.cards[color.value][card_id]
            num = mtuple[2] + 1
            self.cards[color.value][card_id] = (mtuple[0], mtuple[1], num)
        else:
            image = cards_by_colors[color.value][card_id].gui_settings.image.copy()
            rect = image.get_rect().copy()
            rect.left = self.coordinates[color][card_id][0]
            rect.top = self.coordinates[color][card_id][1]
            self.cards[color.value][card_id] = (image, rect, number)
        self.update()
            

    def deleted(self, card_id, color: CardType, number):
        if number == None:
            self.cards[color.value][card_id] = ()
        else:
            m_tuple = self.cards[color.value][card_id]
            num = m_tuple[2] - 1
            self.cards[color.value][card_id] = (m_tuple[0], m_tuple[1], num)
            
        self.update()
            

    def update(self):
        self.board.fill(0xD9D9D9)
        for color in CardType:
            for card_id in self.cards[color.value]:
                if self.cards[color.value][card_id] != () and self.cards[color.value][card_id][2] > 0:
                    image = self.cards[color.value][card_id][0]
                    rect = self.cards[color.value][card_id][1]
                    number = self.cards[color.value][card_id][2]
                    number_surface, number_rect = self.get_multyplyer(number, rect)
                    self.board.blit(image, rect)
                    self.board.blit(number_surface, number_rect)
    
    def blitme(self, screen):
        screen.screen.blit(self.board, self.rect)
        if self.is_border:
            pygame.draw.rect(screen.screen, self.border_color, self.card_border_rect, width=5)
        

    def click(self, x, y):
        x -= self.rect.left
        y -= self.rect.top
        for color in CardType:
            for card_id in self.cards[color.value]:
                if self.cards[color.value][card_id] == ():
                    continue

                if self.cards[color.value][card_id][1].collidepoint(x, y):
                    dispatch_event('card', color, card_id)

    def hover(self, x, y):
        for color in CardType:
            for card_id in self.cards[color.value]:
                if self.cards[color.value][card_id] == ():
                    continue
                card_rect = self.cards[color.value][card_id][1]

                if card_rect.collidepoint(x - self.rect.left, y - self.rect.top):
                    self.card_border_rect.left = card_rect.left + self.rect.left
                    self.card_border_rect.top = card_rect.top + self.rect.top
                    self.is_border = True
                    return
                else:
                    self.is_border = False

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

    WIDTH = PLAYER_CARD_BOARD_WIDTH
    HEIGHT = PLAYER_CARD_BOARD_HEIGHT
    TOP = PLAYER_CARD_BOARD_TOP
    playres_boards = {
        0 : (IND,                   TOP),
        1 : (IND + WIDTH + IND,     TOP),
        2 : (IND + 2*WIDTH + 2*IND, TOP)
    }

    def __init__(self, id, name):
        super().__init__()
        self.cards = [{}, {}, {}, {}, {}]
        self.board = Surface((self.WIDTH, self.HEIGHT))
        self.rect = self.board.get_rect()
        self.player_id = id
        self.active_player_id = -1
        set_handler('active_player', self.new_active_player)

        self.border = Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(self.border, self.border_color, self.rect, width=2)

        self.rect.left = self.playres_boards[id][0]
        self.rect.top = self.playres_boards[id][1]

        self.money_surface = Surface((CARD_MINI_WIDTH, CARD_MINI_HEIGHT))
        self.money_rect = self.money_surface.get_rect()
        self.money_rect.right = self.WIDTH - INDENT
        self.money_rect.bottom = self.HEIGHT - INDENT

        self.player_name_surface = Surface((CARD_MINI_WIDTH*2, 20))
        self.player_name_surface.fill(0xD9D9D9)
        self.player_name_rect = self.player_name_surface.get_rect()
        self.player_name_rect.right = self.WIDTH - INDENT
        self.player_name_rect.top = INDENT
        blit_text(self.player_name_surface, str(name), (0,0), self.FONT, pygame.Color('red'))
        self.player_name_border = Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(self.player_name_border, self.border_color, self.player_name_rect, width=1)

    def new_active_player(self, active_player):
        self.active_player_id = active_player.id

    def added(self, card_id, color: CardType, number):
        if self.cards[color.value].get(card_id) != None:
            mtuple = self.cards[color.value][card_id]
            num = mtuple[2] + 1
            self.cards[color.value][card_id] = (mtuple[0], mtuple[1], num)
        else:
            image = cards_by_colors[color.value][card_id].gui_settings.image_mini.copy()
            rect = image.get_rect().copy()
            rect.left = self.coordinates[color][card_id][0]
            rect.top = self.coordinates[color][card_id][1]
            self.cards[color.value][card_id] = (image, rect, number)
        self.update()

    def deleted(self, card_id, color: CardType, number):
        if number == None:
            self.cards[color.value][card_id] = ()
        else:
            m_tuple = self.cards[color.value][card_id]
            num = m_tuple[2] - 1
            self.cards[color.value][card_id] = (m_tuple[0], m_tuple[1], num)
            
        self.update()

    def money(self, money):
        self.money_surface.fill(0xD9D9D9)
        blit_text(self.money_surface, str(money), (0,0), self.FONT)
        self.board.blit(self.money_surface, self.money_rect)

    def get_multyplyer(self, number, card_rect):
        surface = Surface((16, 16), pygame.SRCALPHA)
        rect = surface.get_rect()
        rect.right = card_rect.right
        rect.top = card_rect.top
        blit_text(surface, str(number), (0,0), self.FONT)
        return surface, rect

    def update(self):
        self.board.fill(0xD9D9D9)
        for color in CardType:
            for card_id in self.cards[color.value]:
                if self.cards[color.value][card_id] != () and self.cards[color.value][card_id][2] > 0:
                    image = self.cards[color.value][card_id][0]
                    rect = self.cards[color.value][card_id][1]
                    number = self.cards[color.value][card_id][2]
                    number_surface, number_rect = self.get_multyplyer(number, rect)
                    self.board.blit(image, rect)
                    self.board.blit(number_surface, number_rect)
        self.board.blit(self.player_name_surface, self.player_name_rect)

    def blitme(self, screen):
        screen.screen.blit(self.board, self.rect)
        if self.is_border:
            screen.screen.blit(self.border, self.rect)
        if self.player_id == self.active_player_id:
            screen.screen.blit(self.player_name_border, self.rect)

    def click(self):
        pass

    def clickable(self):
        return True

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

class Shop:
    def __init__(self):
        self.cards = [{}, {}, {}, {}, {}]
        self.big_card_board = CardBoard()

        for color in CardType:
            for card_id, card in list(crds.cards_by_colors[color.value].items()):
                self.add_card(card_id, color, 6)
        self.is_active = False
        set_handler('shop', self.shop_active)
        set_handler("player_clicked", self.player_clicked)

    def player_clicked(self, _):
        self.is_active = False

    def shop_active(self):
        self.is_active = True

    def add_card(self, card_id, color: CardType, number):
        colored_cards = self.cards[color.value]
        colored_cards[card_id] = 6
        self.big_card_board.added(card_id, color, colored_cards[card_id])

    def del_card(self, card_id, color: CardType):
        colored_cards = self.cards[color.value]
        number = colored_cards.get(card_id)
        if number != None:
            if colored_cards[card_id] > 1:
                colored_cards[card_id] -= 1

                self.big_card_board.deleted(card_id, color, colored_cards[card_id])
            else:
                del colored_cards[card_id]
                
                self.big_card_board.deleted(card_id, color, None)

class MainInfoLine(GObject):
    WIDTH = MAIN_INFO_LINE_WIDTH
    HEIGHT = MAIN_INFO_LINE_HEIGHT
    TOP = MAIN_INFO_LINE_TOP
    LEFT = MAIN_INFO_LINE_LEFT
    def __init__(self):
        super().__init__()
        self.board = Surface((self.WIDTH, self.HEIGHT))
        self.rect = self.board.get_rect()
        self.rect.left = self.LEFT
        self.rect.top = self.TOP

    def blitme(self, screen):
        screen.screen.blit(self.board, self.rect)

    def click(self, x, y):
        pass
