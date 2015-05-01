import logging
import pygame
import random
from pygame.locals import *
from menu import MainMenu, PreGameMenu
from constants import *


class World():
    def __init__(self, screen, map_type, player1, player2):
        self.screen = screen
        self.objects = []
        self.map_type = map_type
        self.font = pygame.font.Font("fonts/8bitwonder.ttf", 14)

        if map_type == "grass":
            print player1 + " vs " + player2
            #Create sprite for ground
            self.ground_sprite = pygame.image.load("images/grass.png")
            

            #Draw ground sprites
            for x in range(0, SCREEN_SIZE[0], self.ground_sprite.get_width()):
                for y in range(0, SCREEN_SIZE[1], self.ground_sprite.get_height()):
                    self.screen.blit(self.ground_sprite, (x, y))

            # TODO
            # 1. Store which WorldObjects and how many of each type that shall be used 
            #    in this map_type
            # 2. Create subclasses for each object
            # 3. Draw background/ environment/ map/ terrain/ WHATEVER

        elif map_type == "sand":
            print player1 + " vs " + player2
            self.ground_sprite = pygame.image.load("images/sand.png")
            self.objects.append((pygame.image.load("images/deadtree.png"), (random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1]))))
            self.objects.append((pygame.image.load("images/deadtree.png"), (random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1]))))
            self.objects.append((pygame.image.load("images/deadtree.png"), (random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1]))))
            self.objects.append((pygame.image.load("images/deadtree.png"), (random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1]))))


        else: #Add more map_types here
        	pass

    def draw(self):

        for x in range(0, SCREEN_SIZE[0], self.ground_sprite.get_width()):
            for y in range(0, SCREEN_SIZE[1], self.ground_sprite.get_height()):
                self.screen.blit(self.ground_sprite, (x,y))
    	

        for obj in self.objects:
        	self.screen.blit(*obj)

    def draw_objects(self):
        for obj in WorldObject.List:
            obj.draw()

class WorldObject(object):

    List = []

    def __init__(self):
        self.path = "images/"

        self.x, self.y = 0,0
        self.name = "Undefined WorldObject"

        WorldObject.List.append(self)

    def draw(self):
        self.screen.blit(self.sprite, (self.x, self.y))

class Bush(WorldObject):

    def __init__(self, filename):
        WorldObject.__init__(self)

        self.name = "Bush"
        self.sprite = pygame.image.load(self.path + filename)
