import pygame
import math
from constants import *
from sound import *
from ammo import *

class Player():
    """The tank controlled by players"""
    def __init__(self, controller, color, k_right, k_backward, k_left, k_forward, k_weapon1, k_weapon2, x, y, rotation = 0):
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
        self.rotation = rotation
        self.direction = None
        self.moving = False
        self.rotating = False
        self.solid = 100
        self.current_collisions = []
        self.dead = False

        """Gives the player static ammo object, these objects are copied in their fire() function.
        These variables can be seen as weapons, so fiddle with these variables when adding/changing it"""
        self.ammo1, self.ammo2 = NormalShot(self), StickyBomb(self)

        if TANK_WIDTH > TANK_HEIGHT:
            self.radius = int(TANK_WIDTH * 0.55)
        else:
            self.radius = int(TANK_HEIGHT * 0.55)

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
            self.ammo1.fire()

    def weapon2(self, event):
        """Fire weapon from slot 2"""
        if not self.dead:
            self.ammo2.fire()

    def move(self):
        """Updates posisition of player. Use different rules for movement when player is colliding"""

        if self.direction == "Forward": #If the player is moving forward, subtract from x, add to y
            self.x -= math.cos(math.radians(self.rotation)) * self.speed
            self.y += math.sin(math.radians(self.rotation)) * self.speed
            if self.speed > self.max_speed:
                self.speed -= self.acceleration
        elif self.direction == "Backward": #If the player is moving backward, add to x, subtract from y
            self.x += math.cos(math.radians(self.rotation)) * self.speed
            self.y -= math.sin(math.radians(self.rotation)) * self.speed
            if self.speed > self.max_speed_back:
                self.speed -= self.acceleration        

        if self.moving == False and self.speed > 0: #Retardate if player isnt pressing keys
            self.speed -= self.acceleration

        if self.speed == 0: #If the players current speed is 0, set the moving direction to None
            self.direction = None

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

            self.max_speed = TANK_SPEED
            self.max_speed_back = TANK_SPEED_BACK
            
            if self.moving or self.rotating:
                if self.animationindex != (len(self.MasterSprites) - 1) * ANIMATION_SPEED:
                    self.animationindex += 1
                else:
                    self.animationindex = 0

            self.detect_collisions()
            self.handle_collisions()
            self.move()
            self.sprite = pygame.transform.rotate(self.MasterSprites[self.animationindex/ANIMATION_SPEED], self.rotation)

        if self.health <= 0:
            self.die()

        """Call the tick() function to update cooldowns"""
        for ammo in [self.ammo1, self.ammo2]:
            ammo.tick()

        """Resetting some atributes each frame"""
        self.rotation_speed = TANK_ROTATION_SPEED
        self.current_collisions = []

    def handle_collisions(self):
        """Handle the agent's current collisions. Also make sure that players can't drive through 
           WorldObjects or outside of the maps borders by using a pushback"""
        for obj in self.current_collisions:
            if obj.type == 50: #if the obj is a powerup
                obj.pickup(self)

            if obj.solid == 100:
                self.speed = 0
                deltax = (self.x - obj.x)
                deltay = (obj.y - self.y)
                self.x += (deltax/3) * SOLID_OBJ_PUSHBACK
                self.y -= (deltay/3) * SOLID_OBJ_PUSHBACK

            else:   #Player will lose speed depending on how solid the WorldObject is
                if (TANK_SPEED - (TANK_SPEED * (obj.solid/100.0))) < self.max_speed:
                    self.max_speed = TANK_SPEED - (TANK_SPEED * (obj.solid/100.0))
                    self.max_speed_back = TANK_SPEED_BACK - (TANK_SPEED_BACK * (obj.solid/100.0))

        if self.x > SCREEN_SIZE[0]-self.radius or self.x < self.radius or self.y > SCREEN_SIZE[1]-self.radius or self.y < self.radius:
            self.speed = 0

            if self.x > SCREEN_SIZE[0]-self.radius:
                self.x -= 10 * MAP_BORDER_PUSHBACK
            elif self.x < self.radius:
                self.x += 10 * MAP_BORDER_PUSHBACK
            elif self.y > SCREEN_SIZE[1]-self.radius:
                self.y -= 10 * MAP_BORDER_PUSHBACK
            else:
                self.y += 10 * MAP_BORDER_PUSHBACK

    def detect_collisions(self):
        """Detect collisions between the player and WorldObjects or other player"""

        for obj in self.controller.map.objects:
            if detect_collision(self, obj):
                self.current_collisions.append(obj)
        
        for player in self.controller.agents:
            if player != self:
                other_player = player

        if len(self.controller.agents) == 2:
            if detect_collision(self, other_player):
                self.current_collisions.append(other_player)

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

        """Draw the cooldown bars if any of your ammo1/ammo2 variables are more than 0. Also Drawing the health bars"""
        if not self.dead:
            pygame.draw.rect(self.screen, (COLOR), (self.x - self.sprite.get_width()/2, self.y - 50, self.health * HEALTHBAR_SIZE[0], HEALTHBAR_SIZE[1]))
            if self.ammo1.cd_time > 0:
                pygame.draw.rect(self.screen, (150,150,150), (self.x - self.sprite.get_width()/2, self.y - 52, ((self.ammo1.cd_time + 0.0) / self.ammo1.cooldown) * 50, 2))
            if self.ammo2.cd_time > 0:
                pygame.draw.rect(self.screen, (255,100,100), (self.x - self.sprite.get_width()/2, self.y - 45, ((self.ammo2.cd_time + 0.0) / self.ammo2.cooldown) * 50, 2))

        if self.controller.debug:   #Collision-detection-testing
            pygame.draw.circle(self.screen, (255,0,0), (int(self.x), int(self.y)), self.radius, 2)