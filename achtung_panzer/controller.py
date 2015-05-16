import sys
import pygame
from pygame.locals import *
from constants import *   # constants are CAPITALIZED
import os
from agent import Player
import map
from menu import MainMenu
from sound import *
from animation import *
from functions import *

# Game States
S_MENU = 1
S_GAME = 2
S_UPGRADES = 3

class Controller():
    """The core game logic that switches states and connects all other internal modules"""
    def __init__(self, debug=False):        

        self.debug = debug

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
        self.font = pygame.font.Font("fonts/8BITWONDER.TTF", 14)
        self.keys = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()

        #SELF DEPENDANT
        self.map = map.World(self)
        self.map.generate()
        self.agents = [Player(self, 'green', pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_w, pygame.K_f, pygame.K_g, 100, 100, 180), Player(self, 'purple', pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP, pygame.K_k, pygame.K_l, 900, 600)]
       
        self.register_eventhandler(pygame.QUIT, self.quit)
        self.register_key(pygame.K_ESCAPE, self.quit, singlepress = True)

        self.menu = MainMenu(self)
        Sound.sounds_init()
        Sound.Sounds["menumusic"].play()

        self.displaytime = False
        self.ammo = []

        if self.debug:
            self.displaytime = True

    def run(self):
        """The main game loop"""
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

                self.map.draw()

                for bullet in self.ammo:
                    bullet.update()
                    bullet.draw()

                for player in self.agents:
                    player.update()
                    player.draw()

                for animation in Animation.List:
                    animation.animate()
                    animation.draw()

            """-------------------------------UPGRADES------------------------------------"""

            if self.state == S_UPGRADES:
                pygame.quit()
                sys.exit()

            
            if self.displaytime:
                self.screen.blit(self.font.render(str(int(self.clock.get_fps())), True, (255,255,255)), (10,10))

            pygame.display.flip()
            self.clock.tick(self.fps)


    def quit(self, event):
        pygame.quit()
        sys.exit()
                   
    def start_game(self):
        self.state = S_GAME

    def register_key(self, event_key, callback, singlepress = False):
        """Binds keys to callback-functions"""
        if singlepress == False:
            self.keymap[(event_key)] = callback
        else:
            self.keymap_singlepress[(event_key)] = callback


    def register_eventhandler(self, event_type, callback):
        """Binds events to callback-functions"""
        self.events[event_type] = callback
