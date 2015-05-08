import pygame
import math
from constants import *
from sound import *
from ammo import *

class Player():
    """The tank controlled by players"""
    def __init__(self, controller, color, k_right, k_backward, k_left, k_forward, k_weapon1, k_weapon2, x, y):
        self.controller = controller
        self.screen = self.controller.screen
        self.name = "Agent"
        self.type = 0
        self.x, self.y = x, y
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
        self.can_drive = True
        self.solid = 100
        self.current_collisions = []

        self.dead = False

        if TANK_WIDTH > TANK_HEIGHT:
            self.radius = int(TANK_WIDTH * 0.5)
        else:
            self.radius = int(TANK_HEIGHT * 0.5)

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
        controller.register_key(k_weapon1, self.weapon1, singlepress=True)
        controller.register_key(k_weapon2, self.weapon2, singlepress=True)

    """Keypress-functions are use to handle movement"""

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

    def weapon1(self, event):
        """Fire weapon from slot 1"""
        if not self.dead:
            self.controller.ammo.append(NormalShot(self))
            Sound.Sounds["shoot"].play()

    def weapon2(self, event):
        """Fire weapon from slot 2"""
        if not self.dead:
            self.controller.ammo.append(Mine(self))

    def move(self):
        """Updates posisition of player. Use different rules for movement when player is colliding"""
        if self.direction == "Forward": #If the player is moving forward, subtract from x, add to y
            self.x -= math.cos(math.radians(self.rotation)) * self.speed
            self.y += math.sin(math.radians(self.rotation)) * self.speed
        elif self.direction == "Backward": #If the player is moving backward, add to x, subtract from y
            self.x += math.cos(math.radians(self.rotation)) * self.speed
            self.y -= math.sin(math.radians(self.rotation)) * self.speed

        if self.moving == False and self.speed > 0: #Retardate if player isnt pressing keys
            self.speed -= self.acceleration

        if self.speed == 0: #If the players current speed is 0, set the moving direction to None
            self.direction = None

        self.pushback()

        self.moving = False
        self.rotating = False


    def die(self):
        """Animate death and play sound"""
        self.dead = True
        Animation(self.screen, "explosion", (self.x, self.y), 9)
        Sound.Sounds["explosion"].play()
        self.controller.agents.remove(self)

        
    def update(self):
        """Update the player's attributes, move player, check if still alive"""

        if not self.dead:
            
            if self.moving or self.rotating:
                if self.animationindex != (len(self.MasterSprites) - 1) * ANIMATION_SPEED:
                    self.animationindex += 1
                else:
                    self.animationindex = 0

            self.move()
            self.sprite = pygame.transform.rotate(self.MasterSprites[self.animationindex/ANIMATION_SPEED], self.rotation)

        if self.health <= 0:
            self.die()

        """for pUp in self.controller.map.powerups:
            if self.x > pUp.x and self.x < pUp.x + pUp.image.get_width() and self.y > pUp.y and self.y < pUp.y + pUp.image.get_height():
                pUp.pickup(self)"""

        #Reset attributes each frame
        self.rotation_speed = TANK_ROTATION_SPEED
        self.current_collisions = []

    def pushback(self):
        for obj in self.current_collisions:
            if obj.solid == 100:
                self.speed = 0
                deltax = self.x - obj.x
                deltay = obj.y - self.y
                self.x += deltax * SOLID_OBJ_PUSHBACK
                self.y -= deltay * SOLID_OBJ_PUSHBACK

    def collision(self, collisions):
        """Handle collisions between the player and other object/player"""
        self.current_collisions = collisions

        """for obj in collisions:  #Used for collision-detection-testing
            print "collision with --> {} - {}".format(obj.name, obj.type)"""

    def draw(self):
        """Render the player and other connected graphics (like health-bar or hitbox) on the screen"""
        if self.health < 40:
            COLOR = (181, 53, 53)
        elif self.health < 60:
            COLOR = (232, 148, 14)
        else:
            COLOR = (90, 200, 100)

        self.screen.blit(self.sprite, (self.x - self.sprite.get_width()/2, self.y - self.sprite.get_height()/2))

        if not self.dead:
            pygame.draw.rect(self.screen, (COLOR), (self.x - self.sprite.get_width()/2, self.y - 50, self.health * HEALTHBAR_SIZE[0], HEALTHBAR_SIZE[1]))

        if self.controller.debug:   #Collision-detection-testing
            pygame.draw.circle(self.screen, (255,0,0), (int(self.x), int(self.y)), self.radius, 2)