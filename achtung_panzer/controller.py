import sys
import pygame
from pygame.locals import *
from constants import *   # constants are CAPITALIZED
from agent import Player
from map import World

# Game States
S_MENU = 1
S_GAME = 2
S_UPGRADES = 3

class Controller():

    def __init__(self):
        self.state = S_GAME
        self.caption = CAPTION
        self.fps = FPS

        self.keymap = {} #REGISTER KEPRESS CONSTANTLY
        self.keymap_singlepress = {} #REGISTER KEYPRESS ONE TIME
        self.events = {} #REGISTER EVENT

        #PYGAME INIT REQUIRED
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.font = pygame.font.SysFont('monospace', 14)
        self.keys = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()

        #SELF DEPENDANT
        self.map = World(self.screen, "grass")
        self.agents = [Player(self.screen, 'blue', self, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_w), Player(self.screen, 'green', self, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP)]

        self.register_eventhandler(pygame.QUIT, self.quit)
        self.register_key(pygame.K_ESCAPE, self.quit, singlepress = True)

    def run(self):

        while True:

            self.keys = pygame.key.get_pressed()

            if self.state == S_MENU:
                pass

            if self.state == S_GAME:

                for event in pygame.event.get():
                    for event_type, callback in self.events.iteritems():
                        if event.type == event_type:
                            callback()

                    if event.type == pygame.KEYDOWN:
                        for event_key in self.keymap_singlepress.iterkeys():
                            if event.key == event_key:
                                self.keymap_singlepress[(event_key)]()

                for event_key in self.keymap.iterkeys():
                    if self.keys[event_key]:
                        self.keymap[(event_key)]()

                self.map.draw()

                for player in self.agents:
                    player.update()
                    player.draw()

                pygame.display.flip()
                self.clock.tick(self.fps)

            if self.state == S_UPGRADES:
                pass

    def register_key(self, event_key, callback, singlepress = False):
        if singlepress == False:
            self.keymap[(event_key)] = callback
        else:
            self.keymap_singlepress[(event_key)] = callback

    def register_eventhandler(self, event_type, callback):
        self.events[event_type] = callback

    def quit(self):
        pygame.quit()
        sys.exit()
