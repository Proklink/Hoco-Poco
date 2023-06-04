import pygame
from GameManager import Manager

 
def run_game():
    pygame.init()
    game = Manager()

    while True:
        game.events()
        game.update()
        game.draw()
        
if __name__ == "__main__":
    run_game()