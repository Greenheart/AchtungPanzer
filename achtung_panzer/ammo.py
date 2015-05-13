import pygame
import math
from functions import *
from constants import *
from animation import *


class Ammo(object):

    def __init__(self, player, sprite):

        self.type = 0
        self.name = "Ammo"
        self.speed = 1
        self.damage = 1
        self.solid = 0

        self.x = 1
        self.y = 1
        self.sx = 1
        self.sy = 1

        self.width, self.height = 1, 1

        self.sprite = sprite
        self.width = sprite.get_width() 
        self.height = sprite.get_height()

        self.player = player
        self.controller = self.player.controller
        if self.width > self.height:
            self.radius = self.width / 2
        else:
            self.radius = self.height / 2

    def update(self):
        pass

    def collision(self):
        pass

    def draw(self):
        self.player.screen.blit(self.sprite, (self.x - self.width/2, self.y-self.height/2))
        
        if self.controller.debug:
            pygame.draw.circle(self.controller.screen, (255,0,0), (int(self.x), int(self.y)), self.radius, 2)


"""-------------------------------------------------AMMO TYPES-----------------------------------------------------------"""


class Bullet(Ammo):

    def __init__(self, player, speed, damage, width, height, sprite):

        super(Bullet, self).__init__(player, sprite)

        self.x, self.y = player.x, player.y

        self.speed = speed
        self.damage = damage
        self.width, self.height = width, height
        self.sprite = sprite
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
        self.sprite = pygame.transform.rotate(self.sprite, self.player.rotation)

#       self.sprite.set_alpha(100)

        self.sx = -math.cos(math.radians(self.player.rotation)) * self.speed
        self.sy = math.sin(math.radians(self.player.rotation)) * self.speed

    def update(self):       
        self.x += self.sx
        self.y += self.sy

        self.collision()    #Check for and handle current collisions

        if self.x > SCREEN_SIZE[0] or self.x < 0 or self.y > SCREEN_SIZE[1] or self.y < 0:
            self.controller.ammo.remove(self)

    def collision(self):
        """Detect and handle collisions between the bullet-object and players or WorldObjects"""

        for player in self.controller.agents:
            if player != self.player:

                if detect_collision(self, player):  #Detect and handle collisions with Players
                    self.controller.ammo.remove(self)
                    player.health -= self.damage
                    Animation(self.player.screen, "explosion", (self.x, self.y), 4)
                    return  #if collision and cur ammo-object is removed, exit function

        for obj in self.controller.map.objects:  #Detect and handle collisions with WorldObjects
            if detect_collision(self, obj):
                if obj.solid == 100: #Completely solid objects stops bullets
                    self.controller.ammo.remove(self)
                    if obj.health:
                        obj.get_shot(self.damage)
                    return  #if collision and cur ammo-object is removed, exit function

                elif obj.name == "DeadBush":
                    self.x -= self.sx * 0.8
                    self.y -= self.sy * 0.8
                    self.sx -= 10
                    self.sy += 10

        """for obj in collisions:  #Used for collision-detection-testing
            print "collision with --> {} - {}".format(obj.name, obj.type)"""


"""-------------------------------------------------AMMO ENDPOINT-----------------------------------------------------------"""


class NormalShot(Bullet):

    def __init__(self, player):

        speed = 10
        damage = 10
        width = 5
        height = 5
        sprite = pygame.image.load("images/ammo/basic_bullet.png")

        super(NormalShot, self).__init__(player, speed, damage, width, height, sprite)

        self.sprite.set_alpha(200)
        self.radius = 5
        self.name = "NormalShot"


class Mine(Bullet):
    def __init__(self, player):

        speed = 0
        damage = 50
        width = 20
        height = 20
        sprite = pygame.image.load("images/ammo/mine.png")

        super(Mine, self).__init__(player, speed, damage, width, height, sprite)

        self.name = "Mine"


class StickyBomb(Bullet):
    def __init__(self, player):

        speed = 10
        damage = 30
        width = 20
        height = 20
        sprite = pygame.image.load("images/ammo/mine.png")

        super(StickyBomb, self).__init__(player, speed, damage, width, height, sprite)

        self.deacceleration = 0.1
        self.radius = 20
        self.max_distance = 100
        self.startx, self.starty = self.player.x, self.player.y
        self.name = "StickyBomb"

    def update(self):       
        self.x += self.sx
        self.y += self.sy

        deltax = math.fabs(self.x - self.startx)
        deltay = math.fabs(self.y - self.starty)

        if deltax > self.max_distance or deltay > self.max_distance:
            if self.sx > 0:
                self.sx -= math.fabs(self.sx) * self.deacceleration
            else:
                self.sx += math.fabs(self.sx) * self.deacceleration
            if self.sy > 0:
                self.sy -= math.fabs(self.sy) * self.deacceleration
            else:
                self.sy += math.fabs(self.sy) * self.deacceleration

        if self.x > SCREEN_SIZE[0] or self.x < 0 or self.y > SCREEN_SIZE[1] or self.y < 0:
            self.controller.ammo.remove(self)

    def detonate(self):
        for player in self.controller.agents:
            if player != self.player:
                if detect_collision(self, player):
                    player.health -= self.damage

        for obj in self.controller.map.objects:
            if detect_collision(self, obj):
                try:
                    if obj.health:
                        obj.get_shot(self.damage)
                except:
                    pass

        self.controller.ammo.remove(self)
        Animation(self.player.screen, "explosion", (self.x, self.y), 4)