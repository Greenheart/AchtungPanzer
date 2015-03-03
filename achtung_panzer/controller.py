import sys
import pygame
from pygame.locals import *
from constants import *   # constants are CAPITALIZED
import os
from agent import Player
from map import World

# Game States
S_MENU = 1
S_GAME = 2
S_UPGRADES = 3
S_ABOUT = 4
S_SETTINGS = 5

class Controller():

    def __init__(self):
        self.state = S_MENU
        
        ## Centers game window, needs to be before pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        ## Init pygame
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()

        ## Load a lot of sprites

        self.background = pygame.image.load("graphics/menu/background.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_SIZE))

        self.logo = pygame.image.load("graphics/menu/logo.png")
        self.logo = pygame.transform.scale(self.logo, (int(540), int(150.3)))

        self.about_description = pygame.image.load("graphics/menu/about_description.png")
        self.about_description = pygame.transform.scale(self.about_description, (int(540), int(243.6)))

        self.start_button = (pygame.image.load("graphics/menu/startbutton.png"), pygame.image.load("graphics/menu/startbutton_hover.png"))
        self.start_button_state = BTN_INACTIVE

        self.about_button = (pygame.image.load("graphics/menu/aboutbutton.png"), pygame.image.load("graphics/menu/aboutbutton_hover.png"))
        self.about_button_state = BTN_INACTIVE

        self.settings_button = (pygame.image.load("graphics/menu/settingsbutton.png"), pygame.image.load("graphics/menu/settingsbutton_hover.png"))
        self.settings_button_state = BTN_INACTIVE

        self.state = S_MENU
        self.caption = CAPTION
        self.fps = FPS

        self.keymap = {}
        self.events = {}

        #PYGAME INIT REQUIRED
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.font = pygame.font.SysFont('monospace', 14)
        self.keys = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()

        #SELF DEPENDANT
        self.map = World(self.screen, "grass")
        self.agents = [Player(self.screen, self, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_w), Player(self.screen, self, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP)]

        self.register_eventhandler(pygame.QUIT, self.quit)
        self.register_key(pygame.K_ESCAPE, pygame.KEYDOWN, self.quit)


    def run(self):

        while True:

            if self.state == S_MENU:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    if event.type == pygame.MOUSEMOTION:
                        x, y = event.pos
                        if ( x in range(351, 649)) and ( y in range(325, 395)):
                            self.start_button_state = BTN_ACTIVE
                        else:
                            self.start_button_state = BTN_INACTIVE
                        if ( x in range(351, 649)) and ( y in range(410, 480)):
                            self.about_button_state = BTN_ACTIVE
                        else:
                            self.about_button_state = BTN_INACTIVE
                        if ( x in range(351, 649)) and ( y in range(495, 565)):
                            self.settings_button_state = BTN_ACTIVE
                        else:
                            self.settings_button_state = BTN_INACTIVE
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        if ( x in range(351, 649)) and ( y in range(325, 395)):
                            print("Start")
                            self.state = S_GAME
                        if ( x in range(351, 649)) and ( y in range(410, 480)):
                            print("About")
                            self.state = S_ABOUT
                        if ( x in range(351, 649)) and ( y in range(495, 565)):
                            print("Settings")
                            self.state = S_SETTINGS


                ## Blits background and logo
                self.screen.blit(self.background, (0,0))
                self.screen.blit(self.logo, (230,100))

                ## Blits buttons and changes depending on state.
                self.screen.blit(self.start_button[self.start_button_state], (351, 325))
                self.screen.blit(self.about_button[self.about_button_state], (351, 410))
                self.screen.blit(self.settings_button[self.settings_button_state], (351, 495))


            


            if self.state == S_GAME:

                for event in pygame.event.get():
                    for event_type, callback in self.events.iteritems():
                        if event.type == event_type:
                            callback(event)

                    for event_key, event_type in self.keymap.iterkeys():
                        if event.type == event_type and event.key == event_key:
                            self.keymap[(event_key, event_type)](event)

                self.map.draw()

                for player in self.agents:
                    player.update_position()
                    player.draw()

                pygame.display.flip()
                self.clock.tick(self.fps)

            if self.state == S_UPGRADES:
                pygame.quit()
                sys.exit()

            if self.state == S_ABOUT:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        self.state = S_MENU
                self.screen.blit(self.background, (0,0))
                self.screen.blit(self.logo, (230, 100))
                self.screen.blit(self.about_description, (230, 325))


            if self.state == S_SETTINGS:
                pygame.quit()
                sys.exit()

            pygame.display.flip()
            self.clock.tick(60)

    def quit(self, event):
        pygame.quit()
        sys.exit()
                        

    def register_key(self, event_key, event_type, callback):
        self.keymap[(event_key, event_type)] = callback


    def register_eventhandler(self, event_type, callback):
        self.events[event_type] = callback
