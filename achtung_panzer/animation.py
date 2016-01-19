import pygame
from constants import *


class Animation():

    List = []

    def __init__(self, screen, name, xy, speed=5):
        self.screen = screen
        self.animationindex = 0
        self.speed = speed
        self.x = xy[0]
        self.y = xy[1]
        self.sprites = None

        if name == "explosion":
            self.sprites = [pygame.transform.scale(pygame.image.load("images/1.png"), (EXPLOSION_SIZE, EXPLOSION_SIZE)), pygame.transform.scale(pygame.image.load("images/2.png"), (EXPLOSION_SIZE, EXPLOSION_SIZE)), pygame.transform.scale(pygame.image.load("images/3.png"), (EXPLOSION_SIZE, EXPLOSION_SIZE)), pygame.transform.scale(pygame.image.load("images/4.png"), (EXPLOSION_SIZE, EXPLOSION_SIZE)), pygame.transform.scale(pygame.image.load("images/5.png"), (EXPLOSION_SIZE, EXPLOSION_SIZE)), pygame.transform.scale(pygame.image.load("images/6.png"), (EXPLOSION_SIZE, EXPLOSION_SIZE))]

        self.sprite = self.sprites[0]

        Animation.List.append(self)

    def animate(self):
        if self.animationindex != (len(self.sprites) - 1) * self.speed:
            self.sprite = self.sprites[self.animationindex//self.speed]
            self.animationindex += 1
        else:
            Animation.List.remove(self)

    def draw(self):
        self.screen.blit(self.sprite, (self.x - self.sprite.get_width() / 2, self.y - self.sprite.get_height() / 2))
