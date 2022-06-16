import pygame
from Settings import *
import sys, os

class UserInterface():

    def __init__(self, player, number_of_lamps, simple_font):
        self.player = player
        self.font = simple_font

        # Get the lamp image
        self.lamp_image = pygame.image.load(os.path.join(DATA_DIR, "lamp", "lamp0000.png")).convert_alpha()
        rect = self.lamp_image.get_rect()
        self.lamp_image = pygame.transform.scale(self.lamp_image, (rect.width * SCALE_FACTOR, rect.height * SCALE_FACTOR))
        self.lamp_rect = self.lamp_image.get_rect()

        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()

        offset = 50
        self.lamp_rect.topleft = self.screen_rect.topleft
        self.lamp_rect.x += offset
        self.lamp_rect.y += offset

        self.total_number_of_lamps = number_of_lamps
        self.collected_lamps = 0

        self.bar_rect = pygame.rect.Rect(self.lamp_rect.x, self.lamp_rect.y,
            160, 16)

        self.bar_rect.midleft = self.lamp_rect.midright


    def reset_counter(self, maximum_value):
        self.total_number_of_lamps = maximum_value
        self.collected_lamps = 0

    def get_bar_color(self):
        if self.player.remaining_oil > 50:
            return (0, 255, 0)
        elif self.player.remaining_oil > 25:
            return (255, 255, 0)
        else:
            return(255, 0, 0)


    def draw(self, level):
        oil_rect = self.bar_rect.copy()
        oil_rect.width = self.player.remaining_oil / 100 * self.bar_rect.width
        if oil_rect.width > self.bar_rect.width:
            oil_rect.width = self.bar_rect.width
        oil_rect = oil_rect.inflate(-5, -5)

        pygame.draw.rect(self.screen, (0,0,0), self.bar_rect)
        pygame.draw.rect(self.screen, self.get_bar_color() ,oil_rect)
        


        self.screen.blit(self.lamp_image, self.lamp_rect)

        text = "{} / {}".format(self.collected_lamps, self.total_number_of_lamps)

        text_surface = self.font.render(text, False, (255, 255, 255), (0,0,0))
        text_surface.set_colorkey((0,0,0))

        text_rect = text_surface.get_rect()
        text_rect.midbottom = self.lamp_rect.midbottom
        text_rect.y += 20

        self.screen.blit(text_surface, text_rect)


        # Add the Level text
        text_surface = self.font.render("Level " + str(level + 1), False, (255, 255, 255), (0,0,0))
        text_surface.set_colorkey((0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.topright = (WINDOW_SIZE[0], 0)
        text_rect.y += 16
        text_rect.x -= 16

        self.screen.blit(text_surface, text_rect)







