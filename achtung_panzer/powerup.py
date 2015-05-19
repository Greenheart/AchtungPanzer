import random
import pygame
from constants import *


class PowerUp(object):
	def __init__(self, world, x, y):

		self.world = world
		self.type = 50
		self.screen = self.world.screen
		self.x, self.y = x, y
		self.solid = 0

		if x == "random":
			self.x = random.randint(0, SCREEN_SIZE[0])
		else:
			self.x = x

		if y == "random":
			self.y = random.randint(0, SCREEN_SIZE[1])
		else:
			self.y = y

	def pickup(self, player):
		"""Function triggered when player collides with powerup"""
		self.callback(player)
		self.world.objects.remove(self)
		

	def draw(self):
		self.screen.blit(self.image, (self.x - self.width/2, self.y - self.width/2))
		if self.world.controller.debug:
			pygame.draw.circle(self.screen, (255,0,0), (int(self.x), int(self.y)), self.radius, 2)

class Mine(PowerUp):

	def __init__(self, world, x, y):
		super(Mine, self).__init__(world, x, y)

		self.image = pygame.image.load("images/ammo/mine.png")
		self.radius = self.image.get_width() - 20
		self.width, self.height = self.image.get_width(), self.image.get_height()

	def callback(self, player):
		"""The actual callback when powerup is picked up"""
		player.health = 0

class Health(PowerUp):

	def __init__(self, world, x, y):
		super(Health, self).__init__(world, x, y)

		self.image = pygame.image.load("images/ammo/mine.png")
		self.value = 20
		self.radius = self.image.get_width() - 20
		self.width, self.height = self.image.get_width(), self.image.get_height()


	def callback(self, player):
		"""The actual callback when powerup is picked up"""  
		if player.health + self.value > 100:
			player.health = 100
		else:
			player.health += self.value

		







