import pygame
from constants import *

class Player():
    def __init__(self, screen, controller, k_right, k_down, k_left, k_up):
        self.screen = screen
        self.x, self.y = 0,0
        self.speed = TANK_SPEED
        self.direction = 0

        #Load and resize tank img
       	self.sprite = pygame.transform.scale(pygame.image.load("images/tank.png"), (TANK_WIDTH, TANK_HEIGHT))

        controller.register_key(k_right, pygame.KEYUP, self.keypress_right)
        controller.register_key(k_right, pygame.KEYDOWN, self.keypress_right)
        controller.register_key(k_down, pygame.KEYUP, self.keypress_down)
        controller.register_key(k_down, pygame.KEYDOWN, self.keypress_down)
        controller.register_key(k_left, pygame.KEYUP, self.keypress_left)
        controller.register_key(k_left, pygame.KEYDOWN, self.keypress_left)
        controller.register_key(k_up, pygame.KEYUP, self.keypress_up)
        controller.register_key(k_up, pygame.KEYDOWN, self.keypress_up)

    def keypress_right(self, event):
        if event.type == pygame.KEYDOWN:
            self.direction = 3
        if event.type == pygame.KEYUP and self.direction == 3:
            self.direction = 0

    def keypress_down(self, event):
        if event.type == pygame.KEYDOWN:
            self.direction = 6
        if event.type == pygame.KEYUP and self.direction == 6:
            self.direction = 0

    def keypress_left(self, event):
        if event.type == pygame.KEYDOWN:
            self.direction = 9
        if event.type == pygame.KEYUP and self.direction == 9:
            self.direction = 0

    def keypress_up(self, event):
        if event.type == pygame.KEYDOWN:
            self.direction = 12
        if event.type == pygame.KEYUP and self.direction == 12:
            self.direction = 0

    def update_position(self):
        if self.direction == 3:
            self.x += self.speed
        elif self.direction == 6:
            self.y += self.speed
        elif self.direction == 9:
            self.x -= self.speed
        elif self.direction == 12:
            self.y -= self.speed

    def draw(self):
        self.screen.blit(self.sprite, (self.x, self.y))