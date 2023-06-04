import pygame
from Graphics.GInfo import GBase
from Graphics.settings import CARD_HEIGHT, CARD_WIDTH, SPACE_BEETWEN_CARDS, LEFT_RIGHT_SPACE, TOP_BOTTOM_SPACE, TAIL_WIDTH, TAIL_HEIGHT


class Artist():
    def __init__(self, screen, settings):
        self.settings = settings
        self.window = screen
        self.clear_color = (0, 0, 0)
        self.grapfic_objects = []

        x = LEFT_RIGHT_SPACE
        y = TOP_BOTTOM_SPACE
        for j in range(TAIL_HEIGHT):
            for i in range(TAIL_WIDTH):
                self.grapfic_objects.append(GBase(x, y))
                x += SPACE_BEETWEN_CARDS + CARD_WIDTH
            x = LEFT_RIGHT_SPACE
            y += SPACE_BEETWEN_CARDS + CARD_HEIGHT
    
    def set_tiles(self, width, height, x, y, click_handler):
        for j in range(height):
            for i in range(width):
                tail_x = i + x
                tail_y = y + j
                koordinates = tail_y * TAIL_HEIGHT + tail_x
                # self.grapfic_objects[koordinates].set_render(None)
                self.grapfic_objects[koordinates].set_click(click_handler)

    def update(self, new_gobjects):
        for y in range(TAIL_HEIGHT):
            for x in range(TAIL_WIDTH):
                gobject = self.grapfic_objects[y * TAIL_HEIGHT + x]
                ret, generated = gobject.expired()
                if not ret:
                    continue
                self.reset_tiles(gobject.WIDTH, gobject.HEIGHT, x, y, None)
                new_gobjects += generated

        for new_gobj in new_gobjects:
            created_gobj = new_gobj[0](new_gobj[1])
            coordinates = created_gobj.y * TAIL_HEIGHT + created_gobj.x

            created_gobj.set_pos(self.grapfic_objects[coordinates].left, self.grapfic_objects[coordinates].top)
            self.grapfic_objects[coordinates].set_render(created_gobj)
            self.set_tiles(created_gobj.WIDTH, created_gobj.HEIGHT, created_gobj.x, created_gobj.y, created_gobj.click)

    def draw(self):
        self.window.screen.fill(self.clear_color)
        self.window.screen.blit(self.window.image, self.window.rect)

        for y in range(TAIL_HEIGHT):
            for x in range(TAIL_WIDTH):
                self.grapfic_objects[y * TAIL_HEIGHT + x].blitme(self.window)

        pygame.display.flip()