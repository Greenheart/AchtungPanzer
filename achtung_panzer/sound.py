import logging
import pygame
from constants import *

class Sound(object):

    Sounds = {}

    @staticmethod
    def sounds_init(): #Cooldown dialogs name in the Sounds dictionary should begin with "cd". Why? Check the play_random method
        pygame.mixer.pre_init(44100, -16, 5, 2048)
        pygame.mixer.init()

        Sound.Sounds.update({
            "hoverbutton" : MiscFX("hoverbutton.wav"),
            "typewriter" : MiscFX("typewriter.wav"),
            "menumusic" : Music("achtung.wav"),
            "explosion" : gameFX("explosion.wav"),
            "shoot" : gameFX("shoot.wav")
            })

    def __init__(self, filename):

        self.sound = pygame.mixer.Sound(self.path + filename)

    @staticmethod
    def set_volume(volume_, channelnum="all"):

        volume = float(volume_)

        if channelnum == "all":
            for name, obj in Sound.Sounds.items():
                obj.sound.set_volume(volume/100)
        else:
            try:
                pygame.mixer.Channel(channelnum).set_volume(volume/100)
            except:
                pygame.mixer.Channel(channelnum[0]).set_volume(volume/100)
                pygame.mixer.Channel(channelnum[1]).set_volume(volume/100)

    def play(self, loops=1): #Loops = -1 means loop the sound forever
        if not self.channel.get_busy():
            self.channel.play(self.sound, loops)

    def fadeout(self):
        self.sound.fadeout(1500)

    def stop(self):
        self.sound.stop()

class Music(Sound):

    def __init__(self, filename):

        self.path = "audio/music/"
        self.channel = pygame.mixer.Channel(MUSIC_CHANNELS)

        self.channel.set_volume(MUSIC_DEFAULT_VOLUME)

        super(Music, self).__init__(filename)

class gameFX(Sound):

    def __init__(self, filename):
        self.channels = [pygame.mixer.Channel(GAMEFX_CHANNELS[0]), pygame.mixer.Channel(GAMEFX_CHANNELS[1])]
        self.path = "audio/gameFX/"

        for channel in self.channels:
            channel.set_volume(GAMEFX_DEFAULT_VOLUME)

        super(gameFX, self).__init__(filename)

    def play(self):
        if not self.channels[0].get_busy():
            self.channels[0].play(self.sound)
        else:
            self.channels[1].play(self.sound)

class MiscFX(Sound):

    def __init__(self, filename):
        self.channels = [pygame.mixer.Channel(MISCFX_CHANNELS[0]), pygame.mixer.Channel(MISCFX_CHANNELS[1])]
        self.path = "audio/miscFX/"

        for channel in self.channels:
            channel.set_volume(MISCFX_DEFAULT_VOLUME)

        super(MiscFX, self).__init__(filename)

    def play(self):
        if not self.channels[0].get_busy():
            self.channels[0].play(self.sound)
        else:
            self.channels[1].play(self.sound)
