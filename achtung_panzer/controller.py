import sys
import pygame
from pygame.locals import *
from constants import *   # constants are CAPITALIZED
import os
from agent import Player
from map import World
from menu import Menu
from sound import *

# Game States
S_MENU = 1
S_GAME = 2
S_UPGRADES = 3
S_ABOUT = 4
S_SETTINGS = 5

class Controller():

    def __init__(self):        
        ## Centers game window, needs to be before pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'


        self.state = S_MENU
        self.fps = FPS
        self.paused = False

        self.keymap = {} #REGISTER KEPRESS CONSTANTLY
        self.keymap_singlepress = {} #REGISTER KEYPRESS ONE TIME
        self.events = {} #REGISTER EVENT

        #PYGAME INIT REQUIRED
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)
        self.font = pygame.font.Font("fonts/8bitwonder.ttf", 14)
        self.keys = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()

        #SELF DEPENDANT
        self.map = World(self.screen, "grass")
        self.agents = [Player(self.screen, 'blue', self, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_w, pygame.K_f), Player(self.screen, 'green', self, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP, pygame.K_k)]

        self.register_eventhandler(pygame.QUIT, self.quit)
        self.register_key(pygame.K_ESCAPE, self.quit, singlepress = True)

        self.menu = Menu(self)
        Sound.sounds_init()
        Sound.Sounds["menumusic"].play()

        self.displaytime = False


    def run(self):

        while True:

            """-------------------------------MENU------------------------------------"""

            if self.state == S_MENU:
                self.menu.draw()

            self.keys = pygame.key.get_pressed()

            if self.state == S_MENU:
                for event in pygame.event.get():
                    # Handle generic events
                    for event_type, callback in self.events.iteritems():
                        if event.type == event_type:
                            callback(event)

                    # Handle keyboard events
                    if event.type == pygame.KEYDOWN:
                        for event_key in self.keymap_singlepress.iterkeys():
                            if event.key == event_key:
                                self.keymap_singlepress[(event_key)](event)

            """-------------------------------GAME------------------------------------"""

            if self.state == S_GAME:

                if not self.paused:

                    for event in pygame.event.get():
                        for event_type, callback in self.events.iteritems():
                            if event.type == event_type:
                                callback(event)

                        if event.type == pygame.KEYDOWN:
                            for event_key in self.keymap_singlepress.iterkeys():
                                if event.key == event_key:
                                    self.keymap_singlepress[(event_key)](event)

                    for event_key in self.keymap.iterkeys():
                        if self.keys[event_key]:
                            self.keymap[(event_key)]()

                else:
                    pass

                for player in self.agents:
                    player.update(self)
                    player.draw()

                self.map.draw()

            """-------------------------------UPGRADES------------------------------------"""

            if self.state == S_UPGRADES:
                pygame.quit()
                sys.exit()

            """-------------------------------ABOUT------------------------------------"""

            if self.state == S_ABOUT:
                self.menu = Menu()
                self.menu.about()

            """-------------------------------SETTINGS------------------------------------"""

            if self.state == S_SETTINGS:
                self.menu = Menu()
                self.menu.settings()
            
            if self.displaytime:
                self.screen.blit(self.font.render(str(self.clock.get_rawtime()), True, (255,255,255)), (10,10))

            pygame.display.flip()
            self.clock.tick(60)


    def quit(self, event):
        pygame.quit()
        sys.exit()
                   

    def start_game(self):
        self.state = S_GAME

    def register_key(self, event_key, callback, singlepress = False):
        if singlepress == False:
            self.keymap[(event_key)] = callback
        else:
            self.keymap_singlepress[(event_key)] = callback


    def register_eventhandler(self, event_type, callback):
        self.events[event_type] = callback
