import pygame
from constants import *

class World():
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, (100,100,100), (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))