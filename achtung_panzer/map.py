import logging
import pygame
import random
from pygame.locals import *
from menu import MainMenu, PreGameMenu
from powerup import *
import math
from agent import Player
from constants import *
from functions import *


class World():
    """The game world. Connects the logic of all WorldObjects with controller and the rest of the game"""
    def __init__(self, controller, map_type):
        self.screen = controller.screen
        self.controller = controller
        self.objects = []	# Collection of all current World Objects
        self.map_type = map_type
        self.powerups = []
        self.font = pygame.font.Font("fonts/8bitwonder.ttf", 14)

        for pup in range(0, random.randint(0, 10)):
            self.objects.append(Health(self, "random", "random"))

    def generate(self):
        """Generate the game world and it's objects"""
        if self.map_type == "grass":
            self.ground_sprite = pygame.image.load("images/grass.png")
            for i in range(random.randint(1, 5)):
                self.objects.append(Water(self))
            
            for i in range(random.randint(2, 10)):
                self.objects.append(Bush(self))

            for i in range(random.randint(3, 15)):
                self.objects.append(Stone(self))

        elif self.map_type == "sand":
            self.ground_sprite = pygame.image.load("images/sand.png")
            for i in range(random.randint(1, 3)):
                self.objects.append(Water(self))

            for i in range(random.randint(1, 2)):
                self.objects.append(Bush(self))

            for i in range(random.randint(1, 10)):
                self.objects.append(DeadBush(self))

            for i in range(random.randint(3, 10)):
                self.objects.append(Stone(self))

            for i in range(random.randint(10, 20)):
                self.objects.append(DesertStone(self))

        self.ground_sprite_width = self.ground_sprite.get_width()
        self.ground_sprite_height = self.ground_sprite.get_height()

    def draw(self):
        """Draw the game-world and all it's objects"""
        for x in range(0, SCREEN_SIZE[0], self.ground_sprite_width):
            for y in range(0, SCREEN_SIZE[1], self.ground_sprite_height):
                self.screen.blit(self.ground_sprite,(x,y))

        for obj in self.objects:
            obj.draw()


class WorldObject(object):
    """General attributes and methods for all WorldObjects"""
    def __init__(self, world):
        self.screen= world.screen
        self.controller = world.controller
        self.x, self.y = 0,0
        self.name = "Undefined WorldObject"
        self.solid = 0
        self.destroyable = False

    def draw(self):
        """General drawing-function for normal objects"""
        self.screen.blit(self.image, (self.x-self.image.get_width()/2, self.y-self.image.get_height()/2))

        if self.controller.debug:   #Collision-detection-testing
            pygame.draw.circle(self.screen, (255,0,0), (int(self.x), int(self.y)), self.radius, 2)


class Object(WorldObject):
    """Normal objects -> An image that only exists on one coordinate"""
    def __init__(self, world):
        WorldObject.__init__(self, world)
        self.type = 0 #worldobject
        self.name = "Undefined Standard-object"

    def check_spawn_point(self):
        """Makes sure that Normal Objects only spawn on the screen and not on top of other WorldObjects"""
        while True:
            self.x = random.randint(self.radius, SCREEN_SIZE[0]-self.radius)
            self.y = random.randint(self.radius, SCREEN_SIZE[1]-self.radius)
            
            for obj in self.controller.map.objects:
                if detect_collision(self, obj):
                    break   #exit the for-loop and get new pos for self

            else:   #object IS spawning on screen and NOT on top of other WorldObject
                break

    def get_random_sprite(self, sprites_list, folder, width, height):
        """Pick a random sprite from sprites_list and set it as the objects sprite.

        Inputs: 
            * List with strings of filenames of images
            * String with folder-path
            * Width and height of sprite
        Result:
            Set a random sprite for the object"""
        image = random.choice(sprites_list)
        full_path = folder + image
        return pygame.transform.scale(pygame.image.load(full_path), (width, height))

    def get_shot(self, damage):
        """Update health of WorldObject. Remove if it gets destroyed"""
        self.health -= damage
        if self.health <= 0:
            self.controller.map.objects.remove(self) 


class Area(WorldObject):
    """Area Objects that is made out of several smaller circle-objets to take up an area"""
    def __init__(self, world):
        WorldObject.__init__(self, world)
        self.type = 1 #area
        self.circles = []
        self.name = "Undefined Area-object"
        self.area()
        self.solid = 50

    def area(self):
        """Generate area and only do so on screen"""
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
    """These circle-objects make up Area-objects"""
    def __init__(self, x, y, phi, radius):
        self.x = x
        self.y = y
        self.phi = phi
        self.radius = radius


class Water(Area):
    """Spawns in various sizes, shapes and colors"""
    def __init__(self, world):
        Area.__init__(self, world)
        self.color = (0, random.randint(0, 100), random.randint(110, 255))
        self.name = "Water"
        self.solid = 50

    def draw(self):
        for circle in self.circles:
            pygame.draw.circle(self.screen, self.color, (int(circle.x), int(circle.y)), int(circle.radius), 0)


class DeadBush(Object):
    """Only spawning on sand-maps"""
    def __init__(self, world):
        Object.__init__(self, world)
        self.name = "DeadBush"
        self.solid = 20
        self.image = pygame.transform.scale(pygame.image.load("images/deadtree.png"), (DEAD_BUSH_SIZE, DEAD_BUSH_SIZE))
        self.radius = self.image.get_width()/3
        self.check_spawn_point()


class Bush(DeadBush):
    """Spawning on grass- and sand-maps"""
    def __init__(self, world):
        DeadBush.__init__(self, world)
        self.name = 'Bush'
        self.solid = 100
        self.image = pygame.image.load('images/busksten.png')
        self.radius = self.image.get_width()/2
        self.check_spawn_point()


class Stone(Object):
    """Spawning in various shapes, sizes and with randomized sprites depending on world.map_type. 
        Is completely solid --> Can't be driven through"""
    def __init__(self, world):
        Object.__init__(self, world)
        self.name = "Stone"
        self.solid = 100
        self.width = random.randint(80, STONE_MAX_SIZE)
        self.height = self.width #values are the same to not trash image quality or collisions
        self.health = self.width * 4
        sprites_list = ['a10010.png', 'a10011.png', 'a10015.png', 'a10002.png']
        folder = 'images/stones/'
        self.image = self.get_random_sprite(sprites_list, folder, self.width, self.height)
        self.radius = self.image.get_height()/4
        self.check_spawn_point()


class DesertStone(Stone):
    """Much like a Stone, but a different sprite and size"""
    def __init__(self, world):
        Stone.__init__(self, world)
        self.name = "DesertStone"
        self.width = random.randint(50, DESERT_STONE_MAX_SIZE)
        self.height = self.width
        sprites_list = ['c40007.png', 'c30011.png', 'c40000.png', 'c40010.png']
        folder = 'images/stones/'
        self.image = self.get_random_sprite(sprites_list, folder, self.width, self.height)
        self.radius = self.image.get_width()/4
        self.check_spawn_point()