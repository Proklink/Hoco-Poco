from pygame import Surface
from cards import CardType, cards_by_colors
from settings import CARD_HEIGHT, CARD_WIDTH


class CardBoard():
    def __init__(self, screen, cards: list):
        self.screen = screen

        max_cards_by_color_width = 0
        max_colors = 0
        for color in CardType:
            if len(cards[color.value]) != 0:
                max_colors += 1
                if len(cards[color.value]) > max_cards_by_color_width:
                    max_cards_by_color_width = len(cards[color.value])
                
        real_width = max_cards_by_color_width * CARD_WIDTH + (max_cards_by_color_width + 1) * 10
        real_height = max_colors * CARD_HEIGHT + max_colors * 10

        self.width = real_width
        self.height = real_height
        self.board = Surface((self.width, self.height))
        self.board.fill((255, 255, 255))

        accumulated_x = 10
        accumulated_y = 10
        for color in CardType:
            for card_id in cards[color.value]:
                self.board.blit(cards_by_colors[color.value][card_id].gui_settings.image, (accumulated_x, accumulated_y))
                accumulated_x += CARD_WIDTH + 10
            accumulated_x = 10
            accumulated_y += CARD_HEIGHT + 10


    def update(self, bullets):
        """Update the ship's position based on the movement flag."""
        
        pass

    def blitme(self):
        """Draw the ship at its current location."""

        self.screen.screen.blit(self.board, self.board.get_rect())
