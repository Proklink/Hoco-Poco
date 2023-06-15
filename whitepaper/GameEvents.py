import sys, pygame
from InternalEvents import dispatch_event, set_handler

class GameIvents:

    def check_buttons(self, mouse_x, mouse_y):
        dispatch_event("click", mouse_x, mouse_y)

    def check_events(self):
        """Respond to keypresses and mouse events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # elif event.type == pygame.KEYDOWN:
            #     self.check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_buttons(mouse_x, mouse_y)

            # elif event.type == pygame.KEYUP:
            #     self.check_keyup_events(event)

    def run(self):
        self.check_events()
