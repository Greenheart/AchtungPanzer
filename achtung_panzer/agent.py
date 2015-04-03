import pygame
import math
from constants import *
from sound import *

class Player():
    def __init__(self, screen, color, controller, k_right, k_backward, k_left, k_forward, k_shoot):
        self.controller = controller
        self.screen = screen
        self.x, self.y = 300,100
        self.health = 100
        self.max_speed = TANK_SPEED
        self.max_speed_back = TANK_SPEED_BACK
        self.acceleration = TANK_ACCELERATION
        self.rotation_speed = TANK_ROTATION_SPEED
        self.speed = 0
        self.rotation = 0
        self.direction = None
        self.moving = False
        self.rotating = False
        self.bullets = []

        self.explosionsprites = [
        pygame.transform.scale(pygame.image.load("images/1.png"), (EXPLOSION_SIZE, EXPLOSION_SIZE)), pygame.transform.scale(pygame.image.load("images/2.png"), (EXPLOSION_SIZE, EXPLOSION_SIZE)),
        pygame.transform.scale(pygame.image.load("images/3.png"), (EXPLOSION_SIZE, EXPLOSION_SIZE)), pygame.transform.scale(pygame.image.load("images/4.png"), (EXPLOSION_SIZE, EXPLOSION_SIZE)),
        pygame.transform.scale(pygame.image.load("images/5.png"), (EXPLOSION_SIZE, EXPLOSION_SIZE)), pygame.transform.scale(pygame.image.load("images/6.png"), (EXPLOSION_SIZE, EXPLOSION_SIZE))]

        self.explosionindex = 0
        self.dead = False

        #Load and resize tank img with right color
        if color == 'green':
            self.MasterSprites = [pygame.transform.scale(pygame.image.load("images/tankgreen1.png"), (TANK_WIDTH, TANK_HEIGHT)), pygame.transform.scale(pygame.image.load("images/tankgreen2.png"), (TANK_WIDTH, TANK_HEIGHT)), pygame.transform.scale(pygame.image.load("images/tankgreen3.png"), (TANK_WIDTH, TANK_HEIGHT))]
        else:
            self.MasterSprites = [pygame.transform.scale(pygame.image.load("images/tankpurple1.png"), (TANK_WIDTH, TANK_HEIGHT)), pygame.transform.scale(pygame.image.load("images/tankpurple2.png"), (TANK_WIDTH, TANK_HEIGHT)), pygame.transform.scale(pygame.image.load("images/tankpurple3.png"), (TANK_WIDTH, TANK_HEIGHT))]

        self.sprite = self.MasterSprites[0]

        self.animationindex = 0

        controller.register_key(k_right, self.keypress_right)
        controller.register_key(k_forward, self.keypress_forward)
        controller.register_key(k_left, self.keypress_left)
        controller.register_key(k_backward, self.keypress_backward)
        controller.register_key(k_shoot, self.shoot, singlepress=True)

    def keypress_right(self):
        if self.rotation == 0:
            self.rotation = 360

        self.rotation -= self.rotation_speed
        self.rotating = True

    def keypress_left(self):
        if self.rotation == 360:
            self.rotation = 0

        self.rotation += self.rotation_speed
        self.rotating = True

    def keypress_backward(self):
        self.moving = True #Set moving variable to true for the update method

        if self.direction == "Forward":
            self.speed -= self.acceleration
        else:
            self.direction = "Backward"
            if self.speed < self.max_speed_back: #Add acceleration to speed if max speed is not reached
                self.speed += self.acceleration


    def keypress_forward(self):
        self.moving = True

        if self.direction == "Backward":
            self.speed -= self.acceleration
        else:
            self.direction = "Forward"
            if self.speed < self.max_speed:
                self.speed += self.acceleration

    def shoot(self, event):
        speedx = -math.cos(math.radians(self.rotation))
        speedy = math.sin(math.radians(self.rotation))
        x = self.x - math.cos(math.radians(self.rotation)) * self.MasterSprites[0].get_width()/2
        y = self.y + math.sin(math.radians(self.rotation)) * self.MasterSprites[0].get_height()/2
        self.bullets.append([x, y, speedx, speedy])
        Sound.Sounds["shoot"].play()


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
        self.rotating = False

    def die(self):
        self.dead = True

        if self.explosionindex == 1:
            Sound.Sounds["explosion"].play()

        if self.explosionindex != (len(self.explosionsprites) - 1) * EXPLOSION_SPEED:
            self.sprite = self.explosionsprites[self.explosionindex/EXPLOSION_SPEED]
            self.explosionindex += 1
        else:
            self.controller.agents.remove(self)

        
    def update(self):

        if not self.dead:
            
            if self.moving or self.rotating:
                if self.animationindex != (len(self.MasterSprites) - 1) * ANIMATION_SPEED:
                    self.animationindex += 1
                else:
                    self.animationindex = 0

            self.move()
            self.sprite = pygame.transform.rotate(self.MasterSprites[self.animationindex/ANIMATION_SPEED], self.rotation)

            for bullet in self.bullets:
                bullet[0] += bullet[2]
                bullet[1] += bullet[3]

                for player in self.controller.agents:
                    if player != self:
                        if bullet[0] > player.x - self.sprite.get_width()/2 and bullet[0] < player.x + player.sprite.get_width()/2 and bullet[1] > player.y - player.sprite.get_height()/2 and bullet[1] < player.y + player.sprite.get_height()/2:
                            self.bullets.remove(bullet)
                            player.health -= 10

        if self.health <= 0:
            self.die()


        for pUp in self.controller.map.powerups:
            if self.x > pUp.x and self.x < pUp.x + pUp.image.get_width() and self.y > pUp.y and self.y < pUp.y + pUp.image.get_height():
                pUp.pickup(self)


    def draw(self):

        if self.health < 40:
            COLOR = (181, 53, 53)
        elif self.health < 60:
            COLOR = (232, 148, 14)
        else:
            COLOR = (90, 200, 100)

        for bullet in self.bullets:
            pygame.draw.rect(self.screen, (0,0,0), (bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE))

        self.screen.blit(self.sprite, (self.x - self.sprite.get_width()/2, self.y - self.sprite.get_height()/2))

        if not self.dead:
            pygame.draw.rect(self.screen, (COLOR), (self.x - self.sprite.get_width()/2, self.y - 50, self.health * HEALTHBAR_SIZE[0], HEALTHBAR_SIZE[1]))

