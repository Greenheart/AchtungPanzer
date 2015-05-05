import pygame
import random
from powerup import *
import math
from agent import Player
from constants import *

class World():
    def __init__(self, controller):
        self.screen = controller.screen
        self.controller = controller
        self.objects = []       # World objects = (image, (x, y), phi, radius, obj_type) State 0=water, 1=deadtree
        self.map_type = random.choice(['grass', 'sand'])

        if self.map_type == "grass":
            self.ground_sprite = pygame.image.load("images/grass.png")
            for i in range(random.randint(1, 4)):
                self.objects.append(Water(self))
            
            for i in range(random.randint(1, 10)):
                self.objects.append(Bush(self))

            for i in range(random.randint(1, 15)):
                self.objects.append(Stone(self))

        elif self.map_type == "sand":
            self.ground_sprite = pygame.image.load("images/sand.png")
            for i in range(random.randint(1, 3)):
                self.objects.append(Water(self))

            for i in range(random.randint(1, 2)):
                self.objects.append(Bush(self))

            for i in range(random.randint(1, 10)):
                self.objects.append(DeadBush(self))

            for i in range(random.randint(1, 10)):
                self.objects.append(Stone(self))

        self.powerups = []
        """for pup in range(0, random.randint(0, 10)):
            self.powerups.append(Mine(self, "random", "random"))"""

    def draw(self):

        for x in range(0, SCREEN_SIZE[0], self.ground_sprite.get_width()):
            for y in range(0, SCREEN_SIZE[1], self.ground_sprite.get_height()):
                self.screen.blit(self.ground_sprite,(x,y))

        for obj in self.objects:
            obj.draw()

        for powerup in self.powerups:
            powerup.draw()

class WorldObject(object):

    def __init__(self, world):
        self.screen= world.screen
        self.controller = world.controller
        self.x, self.y = 0,0
        self.name = "Undefined WorldObject"
        self.drive_through = False
        self.destroyable = False

    def draw(self):
        self.screen.blit(self.image, (self.x-self.image.get_width()/2, self.y-self.image.get_height()/2))
        #Collision-detection-testing

        if self.controller.debug:
            pygame.draw.circle(self.screen, (255,0,0), (int(self.x), int(self.y)), self.radius, 2)

class Object(WorldObject):
    def __init__(self, world):
        WorldObject.__init__(self, world)
        self.type = 0 #worldobject
        self.name = "Undefined Standard-object"

    def check_spawn_point(self, radius):    #Add collision det. between worldobjects here instead of collison()
        while True: #Only spawn object on screen
            self.x = random.randint(radius, SCREEN_SIZE[0])
            self.y = random.randint(radius, SCREEN_SIZE[0])
            
            if self.x > SCREEN_SIZE[0]-radius or self.x < radius or self.y > SCREEN_SIZE[1]-radius or self.y < radius:
                self.x = random.randint(radius, SCREEN_SIZE[0])
                self.y = random.randint(radius, SCREEN_SIZE[0])
            else:   #object IS spawning on screen
                break

class Area(WorldObject):
    def __init__(self, world):
        WorldObject.__init__(self, world)
        self.type = 1 #area
        self.circles = []
        self.name = "Undefined Area-object"
        self.area()

    def area(self):
        radius = 40
        x = random.randint(radius, SCREEN_SIZE[0]-radius)
        y = random.randint(radius, SCREEN_SIZE[1]-radius)
        phi = random.randint(1,10) * 2 * math.pi
        circle = Circle(x, y, phi, radius)
        self.circles.append(circle)

        for i in range(0, random.randint(15, 30)):
            phi = random.randint(int((self.circles[-1].phi - math.radians(random.randint(1, 360)))), int((self.circles[-1].phi + math.radians(random.randint(1, 360)))))
            x = self.circles[-1].x + math.sin(phi) * radius
            y = self.circles[-1].y + math.cos(phi) * radius

            while True: #Only spawn next circle on screen
                if x > SCREEN_SIZE[0]-radius or x < radius or y > SCREEN_SIZE[1]-radius or y < radius:
                    phi = random.randint(int((self.circles[-1].phi - math.radians(random.randint(1, 360)))), int((self.circles[-1].phi + math.radians(random.randint(1, 360)))))
                    x = self.circles[-1].x + math.sin(phi) * radius
                    y = self.circles[-1].y + math.cos(phi) * radius
                else:   #next pos for circle is on the screen, continue
                    break
            circle = Circle(x, y, phi, radius)
            self.circles.append(circle)

class Circle():
    def __init__(self, x, y, phi, radius):
        self.x = x
        self.y = y
        self.phi = phi
        self.radius = radius

class Water(Area):
    def __init__(self, world):
        Area.__init__(self, world)
        self.color = (0, random.randint(0, 100), random.randint(110, 255))
        self.name = "Water"

    def draw(self):
        for circle in self.circles:
            pygame.draw.circle(self.screen, self.color, (int(circle.x), int(circle.y)), int(circle.radius), 0)

class DeadBush(Object):

    def __init__(self, world):
        Object.__init__(self, world)
        self.name = "DeadBush"
        self.drive_through = True
        self.image = pygame.transform.scale(pygame.image.load("images/deadtree.png"), (DEAD_BUSH_SIZE, DEAD_BUSH_SIZE))
        self.radius = self.image.get_width()/3
        self.check_spawn_point(self.radius)

class Bush(DeadBush):

    def __init__(self, world):
        DeadBush.__init__(self, world)
        self.name = 'Bush'
        self.image = pygame.image.load('images/busksten.png')
        self.radius = self.image.get_width()/2
        self.check_spawn_point(self.radius)

class Stone(Object):
    def __init__(self, world):
        Object.__init__(self, world)
        self.name = "Stone"
        self.width = random.randint(100, STONE_MAX_SIZE)
        self.height = self.width #values are the same to not trash image quality or collisions

        folder = 'images/stones/'
        image = random.choice(['a10010.png', 'a10011.png', 'a10015.png', 'a10002.png'])
        full_path = folder + image
        
        self.image = pygame.transform.scale(pygame.image.load(full_path), (self.width, self.height))
        self.radius = self.image.get_width()/4

        self.check_spawn_point(self.radius)


