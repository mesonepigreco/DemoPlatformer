from time import sleep
import pygame

import sys, os
from Settings import *


class Menu:
    def __init__(self, options = [], font_size = FONT_SIZE_MENU, color = (255, 255, 255)) :
        self.options = options
        self.focus = 0
        self.font = pygame.font.Font(FONT_LOCATION, font_size)
        self.color = color

        self.trigger = 0
        self.timeout = 300
        self.return_timeout = 1000
        self.check_return = 0

        self.sound = pygame.mixer.Sound(os.path.join("data", "sounds", "beep.wav")) 


        self.offset_y = 64

    def update(self):
        keys = pygame.key.get_pressed()
        ticks = pygame.time.get_ticks()
        if ticks - self.trigger > self.timeout:
            
            if (keys[pygame.K_UP]):
                self.sound.play()
                self.focus -= 1
                self.trigger = ticks
            elif (keys[pygame.K_DOWN]):
                self.sound.play()
                self.focus += 1
                self.trigger = ticks


        if self.focus < 0:
            self.focus = 0
        if self.focus >= len(self.options):
            self.focus = len(self.options) - 1
        
        if keys[pygame.K_RETURN] and ticks - self.check_return > self.return_timeout:
            self.check_return = ticks
            return self.options[self.focus]
        return None
            





    def draw(self, screen):
        total_size_y = 0
        text_surfaces = []

        width = screen.get_rect().width
        height = screen.get_rect().height


        for i, opt in enumerate(self.options):
            text_surface = self.font.render(opt, False, self.color, (0,0,0))
            text_surface.set_colorkey((0,0,0))
            text_surfaces.append(text_surface)
            text_rect = text_surface.get_rect()
            total_size_y += text_rect.height
            if i > 0:
                total_size_y += self.offset_y
        
        current_y = 0
        for i, surf in enumerate(text_surfaces):
            rect = surf.get_rect()
            rect.midtop = (width // 2 ,height // 2 - total_size_y // 2 + current_y)
            current_y += rect.height + self.offset_y

            if self.focus == i:
                pygame.draw.rect(screen, (255, 0, 0), rect)


            screen.blit(surf, rect)




