import pygame
import random
import math
from agent import Player
from constants import *

class World():
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.map_type = random.choice(['grass', 'sand'])

        if self.map_type == "grass":
            #Create sprite for ground
            self.ground_sprite = pygame.image.load("images/grass.png")
            

            # TODO
            # 1. Store which WorldObjects and how many of each type that shall be used 
            #    in this map_type
            # 2. Create subclasses for each object
            # 3. Draw background/ environment/ map/ terrain/ WHATEVER

        elif self.map_type == "sand":
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
                self.screen.blit(self.ground_sprite,(x,y))

        for obj in self.objects:
        	self.screen.blit(*obj)

class WorldObject:

    def __init__(self):
        self.path = "images/"
        self.x, self.y = 0,0
        self.name = "Undefined WorldObject"
        self.drive_through = False
        self.destroyable = False

    def draw(self):
        self.screen.blit(self.sprite, (self.x, self.y))

class Object(WorldObject):
    def __init__(self):
        WorldObject.__init__(self)
        self.x, self.y = random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1])
        

class Area(WorldObject):
    def __init__(self):
        WorldObject.__init__(self)
        self.circles = []

    def area(self):
        x = random.randint(0, SCREEN_SIZE[0])
        y = random.randint(0, SCREEN_SIZE[1])
        radius = 40
        phi = random.random() * 2 * math.pi
        circle = (x, y, phi, radius)
        self.circles.append(circle)

        for i in range(0, 15):
            phi = random.randint(int((self.circles[-1][2] - math.radians(50))), int((self.circles[-1][2] + math.radians(50))))
            x = self.circles[-1][0] + math.sin(phi) * radius
            y = self.circles[-1][1] + math.cos(phi) * radius
            circle = (x, y, phi, radius)
            self.circles.append(circle)

class Water(Area):
    def __init__(self):
        Area.__init__(self)
        self.color = (0, random.randint(0, 100), random.randint(110, 255))

    def draw(self, screen):
        for circle in self.circles:
            pygame.draw.circle(screen, self.color, (int(circle[0]), int(circle[1])), circle[3], 0)

    def collision(self):
        pass
        


class Bush(Object):

    def __init__(self, filename):
        Object.__init__(self)

        self.name = "Bush"
        self.sprite = pygame.image.load(self.path + filename)

