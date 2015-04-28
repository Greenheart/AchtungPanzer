import pygame
import math
from constants import *


class Ammo(object):

	def __init__(self, player):

		self.speed = 1
		self.damage = 1

		self.x = 1
		self.y = 1
		self.sx = 1
		self.sy = 1

		self.width, self.height = 1, 1

		self.sprite = pygame.image.load("images/ammo/default.png")

		self.player = player
		self.controller = self.player.controller

	def update(self):
		pass

	def draw(self):
		self.player.screen.blit(self.sprite, (self.x, self.y))


"""-------------------------------------------------AMMO TYPES-----------------------------------------------------------"""


class Bullet(Ammo):

	def __init__(self, player, speed, damage, width, height, sprite):

		super(Bullet, self).__init__(player)

		self.x, self.y = player.x, player.y

		self.speed = speed
		self.damage = damage
		self.width, self.height = width, height
		self.sprite = sprite
		self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
		self.sprite = pygame.transform.rotate(self.sprite, self.player.rotation)

		self.sx = -math.cos(math.radians(self.player.rotation)) * self.speed
		self.sy = math.sin(math.radians(self.player.rotation)) * self.speed

	def update(self):		
		self.x += self.sx
		self.y += self.sy

		for player in self.controller.agents:
			if player != self.player:
				if self.x > player.x - player.sprite.get_width()/2 and self.x < player.x + player.sprite.get_width()/2 and self.y > player.y - player.sprite.get_height()/2 and self.y < player.y + player.sprite.get_height()/2:
					self.controller.ammo.remove(self)
					player.health -= self.damage


"""-------------------------------------------------AMMO ENDPOINT-----------------------------------------------------------"""


class NormalShot(Bullet):

	def __init__(self, player):

		speed = 8
		damage = 10
		width = 5
		height = 5
		sprite = pygame.image.load("images/ammo/basic_bullet.png")

		super(NormalShot, self).__init__(player, speed, damage, width, height, sprite)

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
