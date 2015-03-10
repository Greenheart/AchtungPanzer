import pygame
import math
from constants import *

class Player():
    def __init__(self, screen, color, controller, k_right, k_backward, k_left, k_forward):
        self.screen = screen
        self.x, self.y = 0,0
        self.max_speed = TANK_SPEED
        self.acceleration = TANK_ACCELERATION
        self.rotation_speed = TANK_ROTATION_SPEED
        self.speed = 0
        self.rotation = 0

        self.moving = False

        #Load and resize tank img with right color
        if color == 'blue':
       	    self.MasterSprite = pygame.transform.scale(pygame.image.load("images/tankblue.png"), (TANK_WIDTH, TANK_HEIGHT))
        else:
            self.MasterSprite = pygame.transform.scale(pygame.image.load("images/tankgreen.png"), (TANK_WIDTH, TANK_HEIGHT))

        self.sprite = self.MasterSprite

        controller.register_key(k_right, self.keypress_right)
        controller.register_key(k_forward, self.keypress_forward)
        controller.register_key(k_left, self.keypress_left)
        controller.register_key(k_backward, self.keypress_backward)

    def keypress_right(self):
        if self.rotation == 0:
            self.rotation = 360

        self.rotation -= self.rotation_speed

    def keypress_left(self):
        if self.rotation == 360:
            self.rotation = 0

        self.rotation += self.rotation_speed

    def keypress_backward(self):
        self.moving = True

        if self.speed != self.max_speed:
            self.speed += self.acceleration

        self.x += math.cos(self.rotation * 0.0174532925) * self.speed
        self.y -= math.sin(self.rotation * 0.0174532925) * self.speed

    def keypress_forward(self):
        self.moving = True

        if self.speed != self.max_speed:
            self.speed += self.acceleration

        self.x -= math.cos(self.rotation * 0.0174532925) * self.speed
        self.y += math.sin(self.rotation * 0.0174532925) * self.speed
        

    def update(self):
        if self.moving == False:
            self.speed = 0

        self.sprite = pygame.transform.rotozoom(self.MasterSprite, self.rotation, 1)
        self.moving = False

        print self.speed

    def draw(self):
        self.screen.blit(self.sprite, (self.x, self.y))