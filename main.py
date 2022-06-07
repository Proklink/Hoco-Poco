import pygame
import random
from player import Player
import cards
from common import DISPLAY_HEIGHT, DISPLAY_WIDTH, FPS, BLACK, CARD_HEIGHT, CARD_WIDTH, RED
from Card import Card


pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Hoco-Poco")
clock = pygame.time.Clock()


players = [Player(), Player()]
active_player = 0


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    players[0].update(screen)
    # for i in range(len(players[0].cards)):
    #     players[0].cards[i].update(10 + i * (CARD_WIDTH + 10), DISPLAY_HEIGHT - CARD_HEIGHT)
    #     screen.blit(players[0].cards[i].image, players[0].cards[i].rect)


    # после отрисовки всего, переворачиваем экран
    pygame.display.update()

    