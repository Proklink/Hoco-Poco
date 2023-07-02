import pygame
from GameManager import Manager
from InternalEvents import set_handler

def game_over():
    exit()

def run_game():
    pygame.init()
    game = Manager()
    
    run = True

    set_handler('game_over', game_over)

    while run:
        game.events()
        game.update()
        game.draw()
        
if __name__ == "__main__":
    run_game()