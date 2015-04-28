import pygame
import random
from powerup import *
import math
from agent import Player
from constants import *

class World():
    def __init__(self, screen):
        self.screen = screen
        self.objects = []       # World objects = (image, (x, y), phi, radius, obj_type) State 0=water, 1=deadtree
        self.map_type = random.choice(['grass', 'sand'])

        if self.map_type == "grass":
            #Create sprite for ground
            self.ground_sprite = pygame.image.load("images/grass.png")
            sea = Water()
            sea.area()
            self.objects.append(sea)
            bush_1 = Bush()
            bush_2 = Bush()
            

            # TODO
            # 1. Store which WorldObjects and how many of each type that shall be used 
            #    in this map_type
            # 2. Create subclasses for each object
            # 3. Draw background/ environment/ map/ terrain/ WHATEVER
        elif self.map_type == "sand":
            self.ground_sprite = pygame.image.load("images/sand.png")
            sea = Water()
            sea.area()
            self.objects.append(sea)


        else: #Add more map_types here
        	pass


        self.powerups = []

        """for pup in range(0, random.randint(0, 10)):
            self.powerups.append(Mine(self, "random", "random"))"""

    def collision(self, agent):
        collision_with = []
        for object in self.objects:
            radius = object[3] + agent.radius
            hypotenuse = math.sqrt((math.fabs(float(object[1][0] - agent.x))) + (math.fabs(float(object[1][1] - agent.y))))
            if hypotenuse <= radius:
                pass


        return collison_with


    def draw(self):

        for x in range(0, SCREEN_SIZE[0], self.ground_sprite.get_width()):
            for y in range(0, SCREEN_SIZE[1], self.ground_sprite.get_height()):
                self.screen.blit(self.ground_sprite,(x,y))

        for obj in self.objects:
            if obj.type == 0:
                self.screen.blit(*obj)
            else:
                obj.draw(self.screen)

        for powerup in self.powerups:
            powerup.draw()

class WorldObject(object):

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
        self.type = 0 #worldobject
        self.x, self.y = random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1])
        

class Area(WorldObject):
    def __init__(self):
        WorldObject.__init__(self)
        self.type = 1 #area
        self.circles = []

    def area(self):
        x = random.randint(0, SCREEN_SIZE[0])
        y = random.randint(0, SCREEN_SIZE[1])
        radius = 40
        phi = random.random() * 2 * math.pi
        circle = (None, (x, y), phi, radius, 0)
        self.circles.append(circle)

        for i in range(0, 15):
            phi = random.randint(int((self.circles[-1][2] - math.radians(50))), int((self.circles[-1][2] + math.radians(50))))
            x = self.circles[-1][1][0] + math.sin(phi) * radius
            y = self.circles[-1][1][1] + math.cos(phi) * radius
            circle = (None, (x, y), phi, radius, 0)
            self.circles.append(circle)


class Water(Area):
    def __init__(self):
        Area.__init__(self)
        self.color = (0, random.randint(0, 100), random.randint(110, 255))

    def draw(self, screen):
        for circle in self.circles:
            pygame.draw.circle(screen, self.color, (int(circle[1][0]), int(circle[1][1])), circle[3], 0)


class DeadBush(Object):

    def __init__(self):
        Object.__init__(self)

        self.name = "DeadBush"
        self.image = pygame.image.load("images/deadtree.png")
        self.x = random.randint(0, SCREEN_SIZE[0])
        self.y = random.randint(0, SCREEN_SIZE[0])

class Bush(DeadBush):

    def __init__(self):
        DeadBush.__init__(self)
        self.name = 'Bush'
        self.image = pygame.image.load('images/busksten.png')