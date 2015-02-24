from agent import Player
from map import World
import sys
import pygame
from pygame.locals import *
from constants import *   # constants are CAPITALIZED

# Game States
S_MENU = 1
S_ARENA = 2
S_UPGRADES = 3

class Controller():
    def __init__(self):
        self.state = S_MENU
        
        ## Init pygame
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        pygame.display.set_caption(CAPTION)

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

            if self.state == S_ARENA:
                pass

            if self.state == S_UPGRADES:
                pass


                        

