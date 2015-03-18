import pygame
import random
from constants import *

class World():
    def __init__(self, screen, map_type):
        self.screen = screen
        self.objects = []

        if map_type == "grass":
            #Create sprite for background --> grassishch
            self.ground_sprite = pygame.image.load("images/grass.png")
            self.objects.append((pygame.image.load("images/busksten.png"), (random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1]))))

        elif map_type == "sand":
            self.ground_sprite = pygame.image.load("images/sand.png")
            self.objects.append((pygame.image.load("images/deadtree.png"), (random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1]))))
            self.objects.append((pygame.image.load("images/deadtree.png"), (random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1]))))
            self.objects.append((pygame.image.load("images/deadtree.png"), (random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1]))))
            self.objects.append((pygame.image.load("images/deadtree.png"), (random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1]))))

        else: #Add more map_types here
        	pass

    def draw(self):
    	#Draw ground sprites
    	for x in range(0, SCREEN_SIZE[0], self.ground_sprite.get_width()):
    		for y in range(0, SCREEN_SIZE[1], self.ground_sprite.get_height()):
        		self.screen.blit(self.ground_sprite, (x, y))

        for obj in self.objects:
        	self.screen.blit(*obj)
        	#self.screen.blit()