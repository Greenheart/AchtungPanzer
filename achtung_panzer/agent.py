import pygame
import math
from constants import *

class Player():
    def __init__(self, screen, color, controller, k_right, k_backward, k_left, k_forward, k_shoot):
        self.screen = screen
        self.x, self.y = 0,0
        self.health = 100 
        self.max_speed = TANK_SPEED
        self.acceleration = TANK_ACCELERATION
        self.rotation_speed = TANK_ROTATION_SPEED
        self.speed = 0
        self.rotation = 0
        self.direction = None

        self.bullets = []

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
        controller.register_key(k_shoot, self.shoot, singlepress=True)

    def keypress_right(self):
        if self.rotation == 0:
            self.rotation = 360

        self.rotation -= self.rotation_speed

    def keypress_left(self):
        if self.rotation == 360:
            self.rotation = 0

        self.rotation += self.rotation_speed

    def keypress_backward(self):
        self.moving = True #Set moving variable to true for the update method
        self.direction = "Backward"

        if self.speed != self.max_speed: #Add acceleration to speed if max speed is not reached
            self.speed += self.acceleration

    def keypress_forward(self):
        self.moving = True
        self.direction = "Forward"

        if self.speed != self.max_speed:
            self.speed += self.acceleration

    def shoot(self, event):
        speedx = -math.cos(math.radians(self.rotation)) * BULLET_SPEED
        speedy = math.sin(math.radians(self.rotation)) * BULLET_SPEED
        self.bullets.append([self.x, self.y, speedx, speedy])


    def move(self):
        if self.direction == "Forward": #If the player is moving forward, subtract from x, add to y
            self.x -= math.cos(math.radians(self.rotation)) * self.speed
            self.y += math.sin(math.radians(self.rotation)) * self.speed
        elif self.direction == "Backward": #If the player is moving backward, add to x, subtract from y
            self.x += math.cos(math.radians(self.rotation)) * self.speed
            self.y -= math.sin(math.radians(self.rotation)) * self.speed

        if self.moving == False and self.speed > 0: #Deaccelerate if player isnt pressing keys
            self.speed -= self.acceleration

        if self.speed == 0: #If the players current speed is 0, set the moving direction to None
            self.direction = None

        self.moving = False
        
    def update(self, controller):
        self.move()
        self.sprite = pygame.transform.rotate(self.MasterSprite, self.rotation)

        for player in controller.agents:
            for bullet in self.bullets:
                bullet[0] += bullet[2]
                bullet[1] += bullet[3]

                if player != self:
                    if bullet[0] > player.x - self.sprite.get_width()/2 and bullet[0] < player.x + player.sprite.get_width()/2 and bullet[1] > player.y - player.sprite.get_height()/2 and bullet[1] < player.y + player.sprite.get_height()/2:
                        print 'lol'
                        self.bullets.remove(bullet)
                        player.health -= 10

        if self.health <= 0:
            controller.agents.remove(self)


    def draw(self):

        if self.health < 40:
            self.COLOR = (181, 53, 53)
        elif self.health < 60:
            self.COLOR = (232, 148, 14)
        else:
            self.COLOR = (90, 200, 100)

        for bullet in self.bullets:
            pygame.draw.rect(self.screen, (0,0,0), (bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE))

        self.screen.blit(self.sprite, (self.x - self.sprite.get_width()/2, self.y - self.sprite.get_height()/2))
        pygame.draw.rect(self.screen, (self.COLOR), (self.x - self.sprite.get_width()/2, self.y - 50, self.health * HEALTHBAR_SIZE[0], HEALTHBAR_SIZE[1]))