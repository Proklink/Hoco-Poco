import pygame
from screen import Screen
from settings import Settings
from game_manager import Manager

 
def run_game():
    settings = Settings()
    pygame.init()
    screen = Screen(settings.scr_width,
                    settings.scr_height,
                    settings.scr_caption,
                    settings.scr_image)
    game = Manager(settings, screen)

    while True:
        game.events()
        game.update()
        game.draw()
        
if __name__ == "__main__":
    run_game()