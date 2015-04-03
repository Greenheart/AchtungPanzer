import pygame
from constants import *


class Ammo(object):

	def __init__(self, x, y, sx, sy, player):

		self.speed = 1
		self.damage = 1

		self.x = x
		self.y = y
		self.sx = sx * self.speed
		self.sy = sy * self.speed

		self.player = player
		self.controller = self.player.controller

	def update(self):
		self.x += self.sx
		self.y += self.sy

		for player in self.controller.agents:
			if player != self.player:
				if self.x > player.x - self.sprite.get_width()/2 and self.x < player.x + player.sprite.get_width()/2 and self.y > player.y - player.sprite.get_height()/2 and self.y < player.y + player.sprite.get_height()/2:
					self.controller.ammo.remove(self)
                    player.health -= self.damage

	def draw(self):
		self.player.screen.blit(self.image, (self.x, self.y))


class Bullet(Ammo):

	def __init__(self, x, y, sx, sy, player):

		self.speed = 5
		self.damage = 10

		super(Bullet, Ammo).__init__(x, y, sx, sy, player)

	def draw(self):
		pygame.draw.rect(self.player.screen, (self.x, self.y))