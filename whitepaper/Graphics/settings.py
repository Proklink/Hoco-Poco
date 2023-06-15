import pygame
from pygame.transform import smoothscale
import cards as crds

# OLD_CARD_WIDTH = 156 / 2
# OLD_CARD_HEIGHT = 246 / 2

CARD_WIDTH = 768 / 6
CARD_HEIGHT = 768 / 6

SPACE_BEETWEN_CARDS = 4

LEFT_RIGHT_SPACE = 36
TOP_BOTTOM_SPACE = 14

CARD_MINI_WIDTH = CARD_WIDTH / 3
CARD_MINI_HEIGHT = CARD_HEIGHT / 3

TAIL_WIDTH = 14
TAIL_HEIGHT = 8

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900

TEXT_COLOR = (69, 69, 69)

class GUICardSettings:
    def __init__(self, image, width, height):
        self.image = image
        self.width = width
        self.height = height

class Settings():
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings start
        self.scr_width = SCREEN_WIDTH
        self.scr_height = SCREEN_HEIGHT
        self.scr_caption = "Hoco Poco"
        self.scr_background_image_path = 'images/background.jpg'
        self.scr_image = pygame.image.load(self.scr_background_image_path)
        self.rect = self.scr_image.get_rect()
        self.scr_image = smoothscale(self.scr_image, (self.scr_width, self.scr_height))
        # Screen settings end

        #field settings start
        self.field_image_path = 'images/new_cards_images/blue_cards/field.jpg'
        self.field_image = pygame.image.load(self.field_image_path)
        self.field_image = smoothscale(self.field_image, (CARD_WIDTH, CARD_HEIGHT))
        self.field_width = self.field_image.get_rect().width
        self.field_height = self.field_image.get_rect().height
        crds.blue_cards[0].set_gui_settings(GUICardSettings(self.field_image, self.field_width, self.field_height))
        #field settings end

        #ferma settings start
        self.ferma_image_path = 'images/new_cards_images/blue_cards/ferma.jpg'
        self.ferma_image = pygame.image.load(self.ferma_image_path)
        self.ferma_image = smoothscale(self.ferma_image, (CARD_WIDTH, CARD_HEIGHT))
        self.ferma_width = self.ferma_image.get_rect().width
        self.ferma_height = self.ferma_image.get_rect().height
        crds.blue_cards[1].set_gui_settings(GUICardSettings(self.ferma_image, self.ferma_width, self.ferma_height))
        #ferma settings end

        #forest settings start
        self.forest_image_path = 'images/new_cards_images/blue_cards/forest.jpg'
        self.forest_image = pygame.image.load(self.forest_image_path)
        self.forest_image = smoothscale(self.forest_image, (CARD_WIDTH, CARD_HEIGHT))
        self.forest_width = self.forest_image.get_rect().width
        self.forest_height = self.forest_image.get_rect().height
        crds.blue_cards[2].set_gui_settings(GUICardSettings(self.forest_image, self.forest_width, self.forest_height))
        #forest settings end

        #shahta settings start
        self.shahta_image_path = 'images/new_cards_images/blue_cards/shahta.jpg'
        self.shahta_image = pygame.image.load(self.shahta_image_path)
        self.shahta_image = smoothscale(self.shahta_image, (CARD_WIDTH, CARD_HEIGHT))
        self.shahta_width = self.shahta_image.get_rect().width
        self.shahta_height = self.shahta_image.get_rect().height
        crds.blue_cards[3].set_gui_settings(GUICardSettings(self.shahta_image, self.shahta_width, self.shahta_height))
        #shahta settings end

        #apples settings start
        self.apples_image_path = 'images/new_cards_images/blue_cards/apples.jpg'
        self.apples_image = pygame.image.load(self.apples_image_path)
        self.apples_image = smoothscale(self.apples_image, (CARD_WIDTH, CARD_HEIGHT))
        self.apples_width = self.apples_image.get_rect().width
        self.apples_height = self.apples_image.get_rect().height
        crds.blue_cards[4].set_gui_settings(GUICardSettings(self.apples_image, self.apples_width, self.apples_height))
        #apples settings end

        #GREEN

        #peckarna settings start
        self.peckarna_image_path = 'images/new_cards_images/green_cards/peckarna.jpg'
        self.peckarna_image = pygame.image.load(self.peckarna_image_path)
        self.peckarna_image = smoothscale(self.peckarna_image, (CARD_WIDTH, CARD_HEIGHT))
        self.peckarna_width = self.peckarna_image.get_rect().width
        self.peckarna_height = self.peckarna_image.get_rect().height
        crds.green_cards[0].set_gui_settings(GUICardSettings(self.peckarna_image, self.peckarna_width, self.peckarna_height))
        #peckarna settings end

        #market settings start
        self.market_image_path = 'images/new_cards_images/green_cards/market.jpg'
        self.market_image = pygame.image.load(self.market_image_path)
        self.market_image = smoothscale(self.market_image, (CARD_WIDTH, CARD_HEIGHT))
        self.market_width = self.market_image.get_rect().width
        self.market_height = self.market_image.get_rect().height
        crds.green_cards[1].set_gui_settings(GUICardSettings(self.market_image, self.market_width, self.market_height))
        #market settings end

        #cheesemaker settings start
        self.cheesemaker_image_path = 'images/new_cards_images/green_cards/cheesemaker.jpg'
        self.cheesemaker_image = pygame.image.load(self.cheesemaker_image_path)
        self.cheesemaker_image = smoothscale(self.cheesemaker_image, (CARD_WIDTH, CARD_HEIGHT))
        self.cheesemaker_width = self.cheesemaker_image.get_rect().width
        self.cheesemaker_height = self.cheesemaker_image.get_rect().height
        crds.green_cards[2].set_gui_settings(GUICardSettings(self.cheesemaker_image, self.cheesemaker_width, self.cheesemaker_height))
        #cheesemaker settings end

        #mfabrik settings start
        self.mfabrik_image_path = 'images/new_cards_images/green_cards/mfabrik.jpg'
        self.mfabrik_image = pygame.image.load(self.mfabrik_image_path)
        self.mfabrik_image = smoothscale(self.mfabrik_image, (CARD_WIDTH, CARD_HEIGHT))
        self.mfabrik_width = self.mfabrik_image.get_rect().width
        self.mfabrik_height = self.mfabrik_image.get_rect().height
        crds.green_cards[3].set_gui_settings(GUICardSettings(self.mfabrik_image, self.mfabrik_width, self.mfabrik_height))
        #mfabrik settings end

        #fruttymarket settings start
        self.fruttymarket_image_path = 'images/new_cards_images/green_cards/fruttymarket.jpg'
        self.fruttymarket_image = pygame.image.load(self.fruttymarket_image_path)
        self.fruttymarket_image = smoothscale(self.fruttymarket_image, (CARD_WIDTH, CARD_HEIGHT))
        self.fruttymarket_width = self.fruttymarket_image.get_rect().width
        self.fruttymarket_height = self.fruttymarket_image.get_rect().height
        crds.green_cards[4].set_gui_settings(GUICardSettings(self.fruttymarket_image, self.fruttymarket_width, self.fruttymarket_height))
        #fruttymarket settings end

        #RED

        #cafe settings start
        self.cafe_image_path = 'images/new_cards_images/red_cards/cafe.jpg'
        self.cafe_image = pygame.image.load(self.cafe_image_path)
        self.cafe_image = smoothscale(self.cafe_image, (CARD_WIDTH, CARD_HEIGHT))
        self.cafe_width = self.cafe_image.get_rect().width
        self.cafe_height = self.cafe_image.get_rect().height
        crds.red_cards[0].set_gui_settings(GUICardSettings(self.cafe_image, self.cafe_width, self.cafe_height))
        #cafe settings end

        #restorant settings start
        self.restorant_image_path = 'images/new_cards_images/red_cards/restorant.jpg'
        self.restorant_image = pygame.image.load(self.restorant_image_path)
        self.restorant_image = smoothscale(self.restorant_image, (CARD_WIDTH, CARD_HEIGHT))
        self.restorant_width = self.restorant_image.get_rect().width
        self.restorant_height = self.restorant_image.get_rect().height
        crds.red_cards[1].set_gui_settings(GUICardSettings(self.restorant_image, self.restorant_width, self.restorant_height))
        #restorant settings end
        
        #PURPLE

        #stadion settings start
        self.stadion_image_path = 'images/new_cards_images/purple_cards/stadion.jpg'
        self.stadion_image = pygame.image.load(self.stadion_image_path)
        self.stadion_image = smoothscale(self.stadion_image, (CARD_WIDTH, CARD_HEIGHT))
        self.stadion_width = self.stadion_image.get_rect().width
        self.stadion_height = self.stadion_image.get_rect().height
        crds.purple_cards[0].set_gui_settings(GUICardSettings(self.stadion_image, self.stadion_width, self.stadion_height))
        #stadion settings end

        #busycenter settings start
        self.busycenter_image_path = 'images/new_cards_images/purple_cards/busycenter.jpg'
        self.busycenter_image = pygame.image.load(self.busycenter_image_path)
        self.busycenter_image = smoothscale(self.busycenter_image, (CARD_WIDTH, CARD_HEIGHT))
        self.busycenter_width = self.busycenter_image.get_rect().width
        self.busycenter_height = self.busycenter_image.get_rect().height
        crds.purple_cards[1].set_gui_settings(GUICardSettings(self.busycenter_image, self.busycenter_width, self.busycenter_height))
        #busycenter settings end

        #telecenter settings start
        self.telecenter_image_path = 'images/new_cards_images/purple_cards/telecenter.jpg'
        self.telecenter_image = pygame.image.load(self.telecenter_image_path)
        self.telecenter_image = smoothscale(self.telecenter_image, (CARD_WIDTH, CARD_HEIGHT))
        self.telecenter_width = self.telecenter_image.get_rect().width
        self.telecenter_height = self.telecenter_image.get_rect().height
        crds.purple_cards[2].set_gui_settings(GUICardSettings(self.telecenter_image, self.telecenter_width, self.telecenter_height))
        #telecenter settings end

        #WIN

        #vokzal settings start
        self.vokzal_image_path = 'images/new_cards_images/win_cards/vokzal.jpg'
        self.vokzal_image = pygame.image.load(self.vokzal_image_path)
        self.vokzal_image = smoothscale(self.vokzal_image, (CARD_WIDTH, CARD_HEIGHT))
        self.vokzal_width = self.vokzal_image.get_rect().width
        self.vokzal_height = self.vokzal_image.get_rect().height
        crds.win_cards[0].set_gui_settings(GUICardSettings(self.vokzal_image, self.vokzal_width, self.vokzal_height))
        #vokzal settings end

        #tradecenter settings start
        self.tradecenter_image_path = 'images/new_cards_images/win_cards/tradecenter.jpg'
        self.tradecenter_image = pygame.image.load(self.tradecenter_image_path)
        self.tradecenter_image = smoothscale(self.tradecenter_image, (CARD_WIDTH, CARD_HEIGHT))
        self.tradecenter_width = self.tradecenter_image.get_rect().width
        self.tradecenter_height = self.tradecenter_image.get_rect().height
        crds.win_cards[1].set_gui_settings(GUICardSettings(self.tradecenter_image, self.tradecenter_width, self.tradecenter_height))
        #tradecenter settings end

        #hapinesspark settings start
        self.hapinesspark_image_path = 'images/new_cards_images/win_cards/hapinesspark.jpg'
        self.hapinesspark_image = pygame.image.load(self.hapinesspark_image_path)
        self.hapinesspark_image = smoothscale(self.hapinesspark_image, (CARD_WIDTH, CARD_HEIGHT))
        self.hapinesspark_width = self.hapinesspark_image.get_rect().width
        self.hapinesspark_height = self.hapinesspark_image.get_rect().height
        crds.win_cards[2].set_gui_settings(GUICardSettings(self.hapinesspark_image, self.hapinesspark_width, self.hapinesspark_height))
        #hapinesspark settings end

        #radiotower settings start
        self.radiotower_image_path = 'images/new_cards_images/win_cards/radiotower.jpg'
        self.radiotower_image = pygame.image.load(self.radiotower_image_path)
        self.radiotower_image = smoothscale(self.radiotower_image, (CARD_WIDTH, CARD_HEIGHT))
        self.radiotower_width = self.radiotower_image.get_rect().width
        self.radiotower_height = self.radiotower_image.get_rect().height
        crds.win_cards[3].set_gui_settings(GUICardSettings(self.radiotower_image, self.radiotower_width, self.radiotower_height))
        #radiotower settings end

        #PLAYERS

        #car start
        self.car_image_path = 'images/players/car.png'
        self.car_image = pygame.image.load(self.car_image_path)
        # self.car_image = smoothscale(self.radiotower_image, (CARD_WIDTH, CARD_HEIGHT))
        self.car_width = self.car_image.get_rect().width
        self.car_height = self.car_image.get_rect().height
        #car end

        #ship start
        self.ship_image_path = 'images/players/ship.png'
        self.ship_image = pygame.image.load(self.ship_image_path)
        self.ship_width = self.ship_image.get_rect().width
        self.ship_height = self.ship_image.get_rect().height
        #ship end

        #flight start
        self.flight_image_path = 'images/players/flight.png'
        self.flight_image = pygame.image.load(self.flight_image_path)
        self.flight_width = self.flight_image.get_rect().width
        self.flight_height = self.flight_image.get_rect().height
        #flight end

        #coin start
        self.coin_image_path = 'images/coin.jpg'
        self.coin_image = pygame.image.load(self.coin_image_path)
        self.coin_width = self.coin_image.get_rect().width
        self.coin_height = self.coin_image.get_rect().height
        #coin end

        