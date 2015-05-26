import logging
import sys
import pygame
import random
from pygame.locals import *
from constants import *   # constants are CAPITALIZED
import os
from agent import Player
import map
from menu import MainMenu, PreGameMenu, BetweenGameMenu, AfterGameMenu
from sound import *
from animation import *
from functions import *

# Game States
S_MENU = 1
S_GAME = 2
S_UPGRADES = 3
S_ABOUT = 4
S_SETTINGS = 5
S_PREGAME = 6
S_BETWEENGAME = 7
S_AFTERGAME = 8

class Controller():
    """The core game logic that switches states and connects all other internal modules"""
    def __init__(self, debug=False):        

        self.debug = debug

        ## Centers game window, needs to be before pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'


        self.state = S_MENU
        self.fps = FPS
        self.paused = False
        self.all_player_names = []

        self.wait = 1500 #WAITING TIME AFTER FIRST PLAYER DIES, BEFORE MENU SHOWS UP. IN MILLISECONDS.

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
       
        self.register_eventhandler(pygame.QUIT, self.quit)
        self.register_key(pygame.K_ESCAPE, self.quit, singlepress = True)

        self.menu = MainMenu(self)
        self.pregame_menu = False
        self.betweengame_menu = False
        self.aftergame_menu = False
        Sound.sounds_init()
        Sound.Sounds["menumusic"].play()

        self.displaytime = False
        self.ammo = []

        self.maps = ["grass", "sand"]

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

            """-------------------------------PREGAME MENU-----------------------------"""

            self.keys = pygame.key.get_pressed()

            if self.state == S_PREGAME:
                if self.pregame_menu == False:
                    del(self.menu)
                    self.menu = False
                    self.pregame_menu = PreGameMenu(self)

                self.pregame_menu.draw()

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

                if len(self.agents) < 2:
                    if self.wait > 0:
                        self.wait -= self.clock.get_time()
                    else:
                        self.wait = 1500
                        if len(self.agents) == 1:
                            self.stats.inform(self.agents[0].name, score = 1)
                            logging.debug(self.stats.data)
                            self.agents[0].dead = True
                        else:
                            print ("draw")

                        print str(self.stats.data[self.all_player_names[0]].get('score', 0)) + " - " + str(self.stats.data[self.all_player_names[1]].get('score', 0))
                        print 'Distance: {}, Distance: {}'.format(self.stats.data[self.all_player_names[0]].get('move', '--'), 
                                                                  self.stats.data[self.all_player_names[1]].get('move', '--'))
                        print 'Shots: {}, Shots: {}'.format(self.stats.data[self.all_player_names[0]].get('shots_fired', '--'), 
                                                            self.stats.data[self.all_player_names[1]].get('shots_fired', '--'))
                 
                        self.agents = []
                        self.ammo = []
                        Animation.List = []
    #                    if self.round_check(self.score1, self.score2):
    #                        if self.score1 > self.score2:
    #                            print("Purple Wins The Game!")
    #                        else:
    #                            print("Green Wins The Game!")
    #                        self.aftergame_menu = False
    #                        self.state = S_AFTERGAME
    #                    else:
                        self.betweengame_menu = False
                        self.state = S_BETWEENGAME


            """------------------------------BETWEEN-----------------------------------"""
            if self.state == S_BETWEENGAME:
                if self.betweengame_menu == False:
                    del(self.menu)
                    self.menu = False
                    self.betweengame_menu = BetweenGameMenu(self)

                self.betweengame_menu.draw()

            self.keys = pygame.key.get_pressed()

            if self.state == S_BETWEENGAME:
                for event in pygame.event.get():
                    for event_type, callback in self.events.iteritems():
                        if event.type == event_type:
                            callback(event)


                if event.type == pygame.KEYDOWN:
                    for event_key in self.keymap_singlepress.iterkeys():
                        if event.key == event_key:
                            self.keymap_singlepress[(event_key)](event)

            """-------------------------------AFTER---------------------------------------"""
            if self.state == S_AFTERGAME:
                if self.aftergame_menu == False:
                    del(self.menu)
                    self.menu = False
                    self.aftergame_menu = AfterGameMenu(self)

                self.aftergame_menu.draw()

            self.keys = pygame.key.get_pressed()

            if self.state == S_AFTERGAME:
                for event in pygame.event.get():
                    for event_type, callback in self.events.iteritems():
                        if event.type == event_type:
                            callback(event)

                if event.type == pygame.KEYDOWN:
                    for event_key in self.keymap_singlepress.iterkeys():
                        if event.key == event_key:
                            self.keymap_singlepress[(event_key)](event)

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
                self.screen.blit(self.font.render(str(int(self.clock.get_fps())), True, (255,255,255)), (10,10))

            pygame.display.flip()
            self.clock.tick(self.fps)


    def quit(self, event):
        logging.info('Quitting!')
        pygame.quit()
        sys.exit()

    def start_game(self, map_type):
        self.agents = [Player(self, 'green', pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_w, pygame.K_f, pygame.K_g, 100, 100), 
                       Player(self, 'purple', pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP, pygame.K_k, pygame.K_l, 900, 600)]
        self.map = map.World(self, map_type)
        self.map.generate()
        self.stats = Stats(*self.agents)
        self.state = S_GAME

    def continue_game(self):
        self.agents = [Player(self, 'green', pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_w, pygame.K_f, pygame.K_g, 100, 100), 
                       Player(self, 'purple', pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP, pygame.K_k, pygame.K_l, 900, 600)]
        self.agents[0].name = self.all_player_names[0]
        self.agents[1].name = self.all_player_names[1]
        self.map = map.World(self, random.choice(self.maps))
        self.map.generate()
        self.state = S_GAME

    def start_pregame(self):
        self.pregame_menu = False # Make sure there's no old menu
        self.state = S_PREGAME

    def register_key(self, event_key, callback, singlepress = False):
        """Binds keys to callback-functions"""
        if singlepress == False:
            self.keymap[(event_key)] = callback
        else:
            self.keymap_singlepress[(event_key)] = callback


    def register_eventhandler(self, event_type, callback):
        """Binds events to callback-functions"""
        logging.debug('{}: Registering eventhandler ({}, {})'.format(self.__class__.__name__, event_type, callback))
        self.events[event_type] = callback

    def unregister_eventhandler(self, event_type, callback):
        value = self.events.get(event_type)
        if value is not None and value == callback:
            logging.debug('{}: Unregistering eventhandler ({}, {})'.format(self.__class__.__name__, event_type, callback))
            del(self.events[event_type])

class UnknownStatError(Exception):
    pass

class Stats():
    VALID_STATS = ('shots_fired', 'move', 'score')

    def __init__(self, *args):
        self.data = {}

        for player in args:
            self.data[player] = {}


    def inform(self, player, **kwargs):
        # Increments stat with given number. 
        #
        # Example: 
        # inform(player, score = 7)
        #
        # Will increase score stat with 7.
        #
        
        if not (len(kwargs) == 1 and kwargs.keys()[0] in Stats.VALID_STATS):
            raise UnknownStatError('Unknown keyword argument to stat.')

        # Fetch the dictionary associated with player, create a new if it doesn't exist.
        stats = self.data.get(player)
        if stats == None:
            self.data[player] = {}
            stats = self.data[player]

        key, value = kwargs.keys()[0], kwargs.values()[0]

        # Register the stat
        stats[key] = value + stats.get(key, 0)
