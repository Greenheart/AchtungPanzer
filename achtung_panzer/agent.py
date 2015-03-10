import pygame
import math
from constants import *

class Player():
    def __init__(self, screen, color, controller, k_right, k_backward, k_left, k_forward):
        self.screen = screen
        self.x, self.y = 0,0
        self.speed = TANK_SPEED
        self.direction = 0
        self.rotation = 0
        self.desired_rotation = 0
        self.rotating = False

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

        self.rotation -= ROTATION_SPEED
        print self.rotation

    def keypress_left(self):
        if self.rotation == 360:
            self.rotation = 0

        self.rotation += ROTATION_SPEED

        print self.rotation

    def keypress_backward(self):
        self.x += math.cos(self.rotation * 0.0174532925) * TANK_SPEED
        self.y -= math.sin(self.rotation * 0.0174532925) * TANK_SPEED

    def keypress_forward(self):
        self.x -= math.cos(self.rotation * 0.0174532925) * TANK_SPEED
        self.y += math.sin(self.rotation * 0.0174532925) * TANK_SPEED
        

    def update(self):

        self.sprite = pygame.transform.rotozoom(self.MasterSprite, self.rotation, 1)


    def draw(self):
        self.screen.blit(self.sprite, (self.x, self.y))