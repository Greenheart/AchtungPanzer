import pygame, sys
from agent import Player
from map import World
from constants import *

S_MENU = 1
S_GAME = 2

class Controller():

    def __init__(self):
        self.state = S_GAME
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
        self.map = World(self.screen)
        self.agents = [Player(self.screen, self, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_w), Player(self.screen, self, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP)]

        self.register_eventhandler(pygame.QUIT, self.quit)
        self.register_key(pygame.K_ESCAPE, pygame.KEYDOWN, self.quit)

    def run(self):

        while True:

            if self.state == S_MENU:
                pass

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

    def quit(self, event):
        pygame.quit()
        sys.exit()

    def register_key(self, event_key, event_type, callback):
        self.keymap[(event_key, event_type)] = callback

    def register_eventhandler(self, event_type, callback):
        self.events[event_type, callback]