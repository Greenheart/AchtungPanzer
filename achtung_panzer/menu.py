import logging
import pygame
from pygame.locals import *
from constants import *
from sound import *
import os, sys

class Menu():
    def __init__(self, controller):
        self.screen = controller.screen
        self.controller = controller
        self.events = []

        self.background = pygame.image.load("images/menu/background2.jpg")
        self.background = pygame.transform.scale(self.background, (SCREEN_SIZE))

        # Register event at controller
        self.controller.register_eventhandler(pygame.MOUSEMOTION, self.mouse_event)
        self.controller.register_eventhandler(pygame.MOUSEBUTTONDOWN, self.mouse_event)
        self.controller.register_eventhandler(pygame.MOUSEBUTTONUP, self.mouse_event)

    def __del__(self):
        # Register event at controller
        self.controller.unregister_eventhandler(pygame.MOUSEMOTION, self.mouse_event)
        self.controller.unregister_eventhandler(pygame.MOUSEBUTTONDOWN, self.mouse_event)
        self.controller.unregister_eventhandler(pygame.MOUSEBUTTONUP, self.mouse_event)

    def register_eventhandler(self, event_type, state, callback):
        logging.debug('{}: Registering eventhandler ({}, {}, {})'.format(self.__class__.__name__, event_type, state, callback))
        self.events.append((event_type, state, callback))


    def mouse_event(self, event):
        logging.debug('{}: mouse event ({})'.format(self.__class__.__name__, event.type))
        for event_type, state, callback in self.events:
            logging.debug('{}: matching event ({}=={}, {}=={})'.format(self.__class__.__name__, event.type, event_type, state, self.state))
            if event.type == event_type and state == self.state:
                callback(event)

    def draw(self):
        ## Blits background and logo

        self.screen.blit(self.background, (0,0))


class MainMenu(Menu):
    S_MENU_MAIN = 1
    S_MENU_ABOUT = 2
    S_MENU_SETTINGS = 3

    def __init__(self, controller):
        Menu.__init__(self, controller)
 
        self.logo = pygame.image.load("images/menu/logo2.png")

        self.about_description = pygame.image.load("images/menu/about_description.png")

        self.buttons = []
        self.buttons.append(Button(self, self.start_press, MainMenu.S_MENU_MAIN, (351, 325, 649, 395), "images/menu/startbutton.png", "images/menu/startbutton_hover.png"))
        self.buttons.append(Button(self, self.about_press, MainMenu.S_MENU_MAIN, (351, 410, 649, 480), "images/menu/aboutbutton.png", "images/menu/aboutbutton_hover.png"))
        self.buttons.append(Button(self, self.settings_press, MainMenu.S_MENU_MAIN, (351, 495, 649, 565), "images/menu/settingsbutton.png", "images/menu/settingsbutton_hover.png"))
        self.buttons.append(Button(self, self.return_to_main, MainMenu.S_MENU_ABOUT, (351, 575, 649, 645), "images/menu/backbutton.png", "images/menu/backbutton_hover.png"))
        self.buttons.append(Button(self, self.return_to_main, MainMenu.S_MENU_SETTINGS, (351, 575, 649, 645), "images/menu/backbutton.png", "images/menu/backbutton_hover.png"))
        self.buttons.append(Button(self, self.display_time_press, MainMenu.S_MENU_SETTINGS, (351, 475, 649, 545), "images/menu/displaytimebutton.png", "images/menu/displaytimebutton_hover.png"))

        self.sliders = []
        self.sliders.append(Slider(self, self.set_music_volume, MainMenu.S_MENU_SETTINGS, 351, 100, MUSIC_DEFAULT_VOLUME, "Music Volume", "images/menu/knob.png", "images/menu/sliderbg.png"))
        self.sliders.append(Slider(self, self.set_gamefx_volume, MainMenu.S_MENU_SETTINGS, 351, 200, GAMEFX_DEFAULT_VOLUME, "GameFX Volume", "images/menu/knob.png", "images/menu/sliderbg.png"))
        self.sliders.append(Slider(self, self.set_miscfx_volume, MainMenu.S_MENU_SETTINGS, 351, 300, MISCFX_DEFAULT_VOLUME, "MiscFX Volume", "images/menu/knob.png", "images/menu/sliderbg.png"))
        self.sliders.append(Slider(self, self.set_master_volume, MainMenu.S_MENU_SETTINGS, 351, 400, 1, "Master Volume", "images/menu/knob.png", "images/menu/sliderbg.png"))


        self.state = MainMenu.S_MENU_MAIN


    def draw(self):
        ## Blits background and logo

        Menu.draw(self)

        if self.state != MainMenu.S_MENU_SETTINGS:
            self.screen.blit(self.logo, (230,100))

        for button in self.buttons:
            button.draw()

        for slider in self.sliders:
            slider.draw()

        if self.state == MainMenu.S_MENU_ABOUT:
            self.screen.blit(self.about_description, (230, 325))

        for button in self.buttons:
            button.active = True if self.state == button.active_state else False

    def start_press(self, event):
        self.controller.start_pregame()
        self.state = None

    def about_press(self, event):
        self.state = MainMenu.S_MENU_ABOUT

    def settings_press(self, event):
        self.state = MainMenu.S_MENU_SETTINGS

    def return_to_main(self, event):
        self.state = MainMenu.S_MENU_MAIN

    def display_time_press(self, event):
        if self.controller.displaytime:
            self.controller.displaytime = False
        else:
            self.controller.displaytime = True

            
    def set_music_volume(self, volume):
        Sound.set_volume(volume, MUSIC_CHANNELS)

    def set_gamefx_volume(self, volume):
        Sound.set_volume(volume, GAMEFX_CHANNELS)

    def set_miscfx_volume(self, volume):
        Sound.set_volume(volume, MISCFX_CHANNELS)

    def set_master_volume(self, volume):
        Sound.set_volume(volume)

    def settings():
        pygame.quit()
        sys.exit()

"""-------------------PREGAMEMENU------------------"""

class PreGameMenu(Menu):
    S_PREGAME = 1

    def __init__(self, controller):
        Menu.__init__(self, controller)

        self.buttons = []
        self.buttons.append(Button(self, self.startmap_grass, PreGameMenu.S_PREGAME, (25, 100, 325, 300), "images/menu/button_grass.png", "images/menu/button_grass_hover.png"))
        self.buttons.append(Button(self, self.startmap_sand, PreGameMenu.S_PREGAME, (350, 100, 650, 300), "images/menu/button_sand.png", "images/menu/button_sand_hover.png"))

        self.controller.register_eventhandler(pygame.KEYDOWN, self.checkwrite)

        self.state = PreGameMenu.S_PREGAME

        self.player_choice = 1
        self.warning = ""     
        self.player1 = ""
        self.player2 = ""
        self.selector = 585

    def draw(self):

        Menu.draw(self)

        for button in self.buttons:
            button.draw()

#        for slider in self.sliders:
#            slider.draw()

        for button in self.buttons:
            button.active = True if self.state == button.active_state else False

        pygame.draw.rect(self.screen, (0,0,0), (25, 400, 300, 50))
        pygame.draw.rect(self.screen, (0,0,0), (350, 400, 300, 50))
        self.controller.screen.blit(self.controller.font.render(self.player1, True, (255, 255, 255)), (30, 420))
        self.controller.screen.blit(self.controller.font.render(self.player2, True, (255, 255, 255)), (355, 420))
        self.controller.screen.blit(self.controller.font.render(self.warning, True, (0, 0, 0)), (25, 675))
        pygame.draw.rect(self.screen, (255,255,255), (25, self.selector, 500, 30))
        self.controller.screen.blit(self.controller.font.render("Instructions", True, (0, 0, 0)), (25, 550))
        self.controller.screen.blit(self.controller.font.render("Player 1 Enter a name and press enter", True, (0, 0, 0)), (25, 590))
        self.controller.screen.blit(self.controller.font.render("Player 2 Enter a name and press enter", True, (0, 0, 0)), (25, 620))
        self.controller.screen.blit(self.controller.font.render("Select a map", True, (0, 0, 0)), (25, 650))


    def startmap_grass(self, event):
        if self.player1 == self.player2:
            self.warning = "Please enter a valid player name"
            self.player_choice = 1
        else:
            self.player_choice = 3
            self.map_type = "grass"
            self.controller.start_game(self.map_type)
            self.state = None
            self.controller.all_player_names.append(self.player1)
            self.controller.all_player_names.append(self.player2)
            self.controller.agents[0].name = self.player1
            self.controller.agents[1].name = self.player2


    def startmap_sand(self, event):
        if self.player1 == self.player2:
            self.warning = "Please enter a valid player name"
            self.player_choice = 1
        else:
            self.player_choice = 3
            self.map_type = "sand"
            self.controller.start_game(self.map_type)
            self.state = None
            self.controller.all_player_names.append(self.player1)
            self.controller.all_player_names.append(self.player2)
            self.controller.agents[0].name = self.player1
            self.controller.agents[1].name = self.player2

    def checkwrite(self, event):
        if pygame.key.name(event.key) not in ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"):
            pass
        else:
            if self.player_choice == 1:
                if (len(self.player1) < 20):
                    Sound.Sounds["typewriter"].play()
                    self.player1 += pygame.key.name(event.key)
                else:
                    pass
            elif self.player_choice == 2:
                if (len(self.player2) < 20):
                    Sound.Sounds["typewriter"].play()
                    self.player2 += pygame.key.name(event.key)
                else:
                    pass
            else:
                pass

        if pygame.key.name(event.key) == "backspace":
            if self.player_choice == 1:
                Sound.Sounds["typewriter"].play()
                self.player1 = self.player1[:-1]
            elif self.player_choice == 2:
                Sound.Sounds["typewriter"].play()
                self.player2 = self.player2[:-1]
            else:
                pass

        if pygame.key.name(event.key) == "space":
            if self.player_choice == 1:
                Sound.Sounds["typewriter"].play()
                self.player1 += " "
            elif self.player_choice == 2:
                Sound.Sounds["typewriter"].play()
                self.player2 += " "
            else:
                pass

        if pygame.key.name(event.key) == "return":
            self.player_choice += 1
            if self.player_choice == 2:
                self.selector = 610
            elif self.player_choice == 3:
                if self.player1 == self.player2:
                    self.warning = "You can not use the same player name"
                    self.player1 = ""
                    self.player2 = ""
                    self.selector = 585
                    self.player_choice = 1
                else:  
                    self.selector = 640

"""-------------------BETWEENGAMEMENU------------------"""

class BetweenGameMenu(Menu):
    S_BETWEENGAME = 1

    def __init__(self, controller):
        Menu.__init__(self, controller)

        self.buttons = []
        self.buttons.append(Button(self, self.continue_press, BetweenGameMenu.S_BETWEENGAME, (351, 325, 649, 395), "images/menu/startnext.png", "images/menu/startnext_hover.png"))


        self.state = BetweenGameMenu.S_BETWEENGAME

    def draw(self):

        Menu.draw(self)

        for buttons in self.buttons:
            buttons.draw()

        for button in self.buttons:
            button.active = True if self.state == button.active_state else False

        self.controller.screen.blit(self.controller.font.render(str(self.controller.stats.data[self.controller.all_player_names[0]].get('score', 0)) + " - " + str(self.controller.stats.data[self.controller.all_player_names[1]].get('score', 0)), True, (255, 255, 255)), (355, 420))


    def continue_press(self, event):
        self.controller.continue_game()
        self.state = None

"""-------------------AFTERGAMEMENU------------------"""

class AfterGameMenu(Menu):
    S_AFTERGAME = 1

    def __init__(self, controller):
        Menu.__init__(self, controller)

        self.buttons = []
        self.buttons.append(Button(self, self.quit, AfterGameMenu.S_AFTERGAME, (351, 325, 649, 395), "images/menu/exitbutton.png", "images/menu/exitbutton_hover.png"))

        self.state = AfterGameMenu.S_AFTERGAME

    def draw(self):
        
        Menu.draw(self)

        for buttons in self.buttons:
            buttons.draw()

        for button in self.buttons:
            button.active = True if self.state == button.active_state else False

    def quit(self, event):
        pygame.quit()
        sys.exit()

class Button():
    def __init__(self, menu, callback, active_state, coords, image_normal, image_hover):
        self.menu = menu
        self.screen = menu.screen
        self.callback = callback
        self.active = False
        self.active_state = active_state
        self.x1, self.y1, self.x2, self.y2 = coords

        self.hover = False
        self.pressed = False

        self.image_normal = pygame.image.load(image_normal)
        self.image_hover = pygame.image.load(image_hover)

        self.menu.register_eventhandler(pygame.MOUSEMOTION, self.active_state, self.mousemotion)
        self.menu.register_eventhandler(pygame.MOUSEBUTTONDOWN, self.active_state, self.mousebuttondown)

    def mousemotion(self, event):
        x, y = event.pos
        if self.active and x >= self.x1 and x < self.x2 and y >= self.y1 and y < self.y2:
            if not self.hover:
                Sound.Sounds["hoverbutton"].play()
            self.hover = True
        else:
            self.hover = False


    def mousebuttondown(self, event):
        logging.debug('{} button pressed'.format(id(self)))
        x, y = event.pos
        if self.active and x >= self.x1 and x < self.x2 and y >= self.y1 and y < self.y2:
            self.pressed = True
            self.callback(event)
        else:
            self.pressed = False

        self.hover = False

    def draw(self):
        if self.active:
            image = self.image_hover if self.hover else self.image_normal
            self.screen.blit(image, (self.x1, self.y1))

class Slider():
    def __init__(self, menu, callback, active_state, x, y, default_value, caption, knob_image, bg_image):

        self.menu = menu
        self.screen = menu.screen
        self.active_state = active_state
        self.caption = caption
        self.callback = callback

        self.bg_image = pygame.image.load(bg_image)
        self.knob_image = pygame.image.load(knob_image)

        self.bg_x, self.bg_y = x, y
        self.x_min = self.bg_x + 10
        self.x_max = self.bg_x + self.bg_image.get_width() - self.knob_image.get_width() - 10
        self.x = self.x_min + (self.x_max - self.x_min) * default_value
        self.y = self.bg_y + self.bg_image.get_height()/2 - self.knob_image.get_height()/2

        self.selected = False

        self.menu.register_eventhandler(pygame.MOUSEBUTTONDOWN, self.active_state, self.mousebuttondown)
        self.menu.register_eventhandler(pygame.MOUSEBUTTONUP, self.active_state, self.mousebuttonup)
        self.menu.register_eventhandler(pygame.MOUSEMOTION, self.active_state, self.mousemotion)

    def mousebuttondown(self, event):
        x, y = event.pos
        if self.menu.state == self.active_state and x >= self.x and x <= self.x + self.knob_image.get_width() and y >= self.y and y <= self.y + self.knob_image.get_height():
            self.selected = True

    def mousemotion(self, event):
        x, y = event.pos
        if self.selected:
            if self.x >= self.x_min and self.x <= self.x_max:
                self.x = x - (self.knob_image.get_width() / 2)

            if self.x < self.x_min:
                self.x = self.x_min
            elif self.x > self.x_max:
                self.x = self.x_max

            self.callback(self.get_value())

    def mousebuttonup(self, event):
        self.selected = False

    def get_value(self):
        total = self.x_max - self.x_min
        current_value = ((self.x - self.x_min) * 100 / total)   
        return current_value

    def draw(self):
        if self.menu.state == self.active_state:
            self.screen.blit(self.bg_image, (self.bg_x, self.bg_y))
            self.screen.blit(self.knob_image, (self.x, self.y))
            self.screen.blit(self.menu.controller.font.render(self.caption + " " + str(int(self.get_value())), True, (0,0,0)), (self.bg_x + self.bg_image.get_width()/2 - 8 * len(self.caption), self.bg_y - self.bg_image.get_height()/2))

