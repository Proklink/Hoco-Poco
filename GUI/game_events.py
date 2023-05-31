import sys, pygame


def check_keydown_events(event, ship):
    pass
    # ship.check_moving_events_keydown(event)

    # if event.key == pygame.K_SPACE:
    #     ship.shooting = True

def check_keyup_events(event, ship):
    pass
    # ship.check_moving_events_keyup(event)

    # if event.key == pygame.K_SPACE:
    #     ship.shooting = False

def stop_game(game_mngr, stats):
    if stats.game_active:
        stats.game_active = False
        # game_mngr.destroy_game()


def check_events_game_active(game_mngr, ship, stats):
    """Respond to keypresses and mouse events."""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship)
            if event.key == pygame.K_ESCAPE:
                stop_game(game_mngr, stats)
            # if event.key == pygame.K_m:
            #     game_mngr.switch_moving()
            # if event.key == pygame.K_p:
            #     if game_mngr.asters:
            #         game_mngr.asters = False
            #     else:
            #         game_mngr.asters = True
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_events_game_inactive(game_mngr, stats): #нельзя передавать game_manager
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_menu_buttons(game_mngr, stats, mouse_x, mouse_y)

def check_menu_buttons(game_mngr, stats, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    pass
    # if game_mngr.play_button.rect.collidepoint(mouse_x, mouse_y):
    #     game_mngr.init_game()
    #     stats.game_active = True
    # if game_mngr.exit_button.rect.collidepoint(mouse_x, mouse_y):
    #     sys.exit()