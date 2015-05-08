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

#		self.sprite.set_alpha(100)

		self.sx = -math.cos(math.radians(self.player.rotation)) * self.speed
		self.sy = math.sin(math.radians(self.player.rotation)) * self.speed

	def update(self):		
		self.x += self.sx
		self.y += self.sy

		for player in self.controller.agents:
			if player != self.player:

				if detect_collision(self, player):
					self.controller.ammo.remove(self)
					player.health -= self.damage
					Animation(self.player.screen, "explosion", (self.x, self.y), 4)

		if self.x > SCREEN_SIZE[0] or self.x < 0 or self.y > SCREEN_SIZE[1] or self.y < 0:
			self.controller.ammo.remove(self)



"""-------------------------------------------------AMMO ENDPOINT-----------------------------------------------------------"""


class NormalShot(Bullet):

	def __init__(self, player):

		speed = 13
		damage = 10
		width = 5
		height = 5
		sprite = pygame.image.load("images/ammo/basic_bullet.png")

		super(NormalShot, self).__init__(player, speed, damage, width, height, sprite)

		self.sprite.set_alpha(200)
		self.radius = 5


class Mine(Bullet):
	def __init__(self, player):

		speed = 0
		damage = 50
		width = 20
		height = 20
		sprite = pygame.image.load("images/ammo/mine.png")

		super(Mine, self).__init__(player, speed, damage, width, height, sprite)


class AtomicBomb(Bullet):
	def __init__(self, player):

		speed = 0
		damage = 70
		width = 50
		height = 50
		sprite = pygame.image.load("images/ammo/mine.png")

		super(Mine, self).__init__(player, speed, damage, width, height, sprite)
