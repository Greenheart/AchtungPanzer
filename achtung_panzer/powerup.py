import random
import pygame
from constants import *


class PowerUp(object):
	def __init__(self, world, x, y):

		self.world = world
		self.screen = self.world.screen
		self.x, self.y = x, y

		if x == "random":
			self.x = random.randint(0, SCREEN_SIZE[0])
		else:
			self.x = x

		if y == "random":
			self.y = random.randint(0, SCREEN_SIZE[1])
		else:
			self.y = y

	def pickup(self, player):
		self.callback(player)
		self.world.powerups.remove(self)
		

	def draw(self):
		self.screen.blit(self.image, (self.x, self.y))

class Mine(PowerUp):

	def __init__(self, world, x, y):
		super(Mine, self).__init__(world, x, y)

		self.image = pygame.image.load("images/mine.png")

	def callback(self, player):
		player.health = 0

class Health(PowerUp):

	def __init__(self, world, x, y):
		super(Health, self).__init__(world, x, y)

		self.image = pygame.image.load("images/mine.png")
		self.value = 20

	def callback(self, player):
		if player.health + self.value > 100:
			player.health = 100
		else:
			player.health += self.value

		







