import pygame

class Sound(object):

	Sounds = {}

	@staticmethod
	def sounds_init(): #Cooldown dialogs name in the Sounds dictionary should begin with "cd". Why? Check the play_random method
		pygame.mixer.pre_init(44100, -16, 5, 2048)
		pygame.mixer.init()

		Sound.Sounds.update({
			"hoverbutton" : MiscFX("hoverbutton.wav"),
			"menumusic" : Music("iieoho.wav")
			})
	
	def __init__(self, filename):

		self.sound = pygame.mixer.Sound(self.path + filename)

	def play(self, loops=1): #Loops = -1 means loop the sound forever
		if not self.channel.get_busy():
			self.channel.play(self.sound, loops)

	def stop(self):
		self.channel.stop()

class Music(Sound):

	def __init__(self, filename):

		self.path = "audio/music/"
		self.channel = pygame.mixer.Channel(1)

		self.channel.set_volume(0.1)

		super(Music, self).__init__(filename)

class gameFX(Sound):

	def __init__(self, filename):
		self.channels = [pygame.mixer.Channel(2), pygame.mixer.Channel(3)]
		self.path = "audio/gameFX/"

		for channel in self.channels:
			channel.set_volume(0.5)

		super(SpellFX, self).__init__(filename)

	def play(self):
		if not self.channels[0].get_busy():
			self.channels[0].play(self.sound)
		else:
			self.channels[1].play(self.sound)

class MiscFX(Sound):

	def __init__(self, filename):
		self.channels = [pygame.mixer.Channel(4), pygame.mixer.Channel(5)]
		self.path = "audio/miscFX/"

		for channel in self.channels:
			channel.set_volume(0.05)

		super(MiscFX, self).__init__(filename)

	def play(self):
		if not self.channels[0].get_busy():
			self.channels[0].play(self.sound)
		else:
			self.channels[1].play(self.sound)