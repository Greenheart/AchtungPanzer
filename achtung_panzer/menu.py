import pygame
from pygame.locals import *
from constants import *
import os, sys

S_MENU_MAIN = 1
S_MENU_ABOUT = 2
S_MENU_SETTINGS = 3

class Menu():
    def __init__(self, controller):
        self.screen = controller.screen
        self.controller = controller
        self.events = []

        self.background = pygame.image.load("images/menu/background.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_SIZE))

        self.logo = pygame.image.load("images/menu/logo.png")

        self.about_description = pygame.image.load("images/menu/about_description.png")

        self.buttons = []
        self.buttons.append(Button(self, self.start_press, S_MENU_MAIN, (351, 325, 649, 395), "images/menu/startbutton.png", "images/menu/startbutton_hover.png"))
        self.buttons.append(Button(self, self.about_press, S_MENU_MAIN, (351, 410, 649, 480), "images/menu/aboutbutton.png", "images/menu/aboutbutton_hover.png"))
        self.buttons.append(Button(self, self.settings_press, S_MENU_MAIN, (351, 495, 649, 565), "images/menu/settingsbutton.png", "images/menu/settingsbutton_hover.png"))

        self.buttons.append(Button(self, self.return_to_main, S_MENU_ABOUT, (351, 575, 649, 645), "images/menu/backbutton.png", "images/menu/backbutton_hover.png"))


        self.state = S_MENU_MAIN


        # Register event at controller
        self.controller.register_eventhandler(pygame.MOUSEMOTION, self.mouse_event)
        self.controller.register_eventhandler(pygame.MOUSEBUTTONDOWN, self.mouse_event)


    def register_eventhandler(self, event_type, state, callback):
        self.events.append((event_type, state, callback))


    def mouse_event(self, event):
        for event_type, state, callback in self.events:
            if event.type == event_type and state == self.state:
                callback(event)


    def draw(self):
        ## Blits background and logo
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.logo, (230,100))

        for button in self.buttons:
            button.draw()


        if self.state == S_MENU_ABOUT:
            self.screen.blit(self.logo, (230, 100))
            self.screen.blit(self.about_description, (230, 325))

    def start_press(self, event):
        self.controller.start_game()

    def about_press(self, event):
        self.state = S_MENU_ABOUT

    def settings_press(self, event):
        pass

    def return_to_main(self, event):
        self.state = S_MENU_MAIN



    def settings():
        pygame.quit()
        sys.exit()


class Button():
    def __init__(self, menu, callback, active_state, coords, image_normal, image_hover):
        self.menu = menu
        self.screen = menu.screen
        self.callback = callback
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
        if self.menu.state == self.active_state and x >= self.x1 and x < self.x2 and y >= self.y1 and y < self.y2:
            self.hover = True
        else:
            self.hover = False

    def mousebuttondown(self, event):
        x, y = event.pos
        if self.menu.state == self.active_state and x >= self.x1 and x < self.x2 and y >= self.y1 and y < self.y2:
            self.pressed = True
            self.callback(event)
        else:
            self.pressed = False

    def draw(self):
        if self.menu.state == self.active_state:
            image = self.image_hover if self.hover else self.image_normal
            self.screen.blit(image, (self.x1, self.y1))
