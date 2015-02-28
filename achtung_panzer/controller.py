from agent import Player
from map import World
import sys
import pygame
from pygame.locals import *
from constants import *   # constants are CAPITALIZED
import os

# Game States
S_MENU = 1
S_ARENA = 2
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
        self.screen = pygame.display.set_mode(SCREENSIZE)
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()

        ## Load a lot of sprites

        self.background = pygame.image.load("graphics/menu/background.png")
        self.background = pygame.transform.scale(self.background, (SCREENSIZE))

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
                            self.state = S_ARENA
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


            

            if self.state == S_ARENA:
                pygame.quit()
                sys.exit()

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
                        

