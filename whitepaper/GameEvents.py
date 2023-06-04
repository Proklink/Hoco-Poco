import sys, pygame


class GameIvents:
    def check_keydown_events(self, event):
        pass
        # ship.check_moving_events_keydown(event)

        # if event.key == pygame.K_SPACE:
        #     ship.shooting = True

    def check_keyup_events(self, event):
        pass
        # ship.check_moving_events_keyup(event)

        # if event.key == pygame.K_SPACE:
        #     ship.shooting = False

    def check_events(self):
        """Respond to keypresses and mouse events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
                # if event.key == pygame.K_m:
                #     game_mngr.switch_moving()
                # if event.key == pygame.K_p:
                #     if game_mngr.asters:
                #         game_mngr.asters = False
                #     else:
                #         game_mngr.asters = True
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

    def run(self):
        self.check_events()

