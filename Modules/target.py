import pygame
from Modules.Settings import DATA_DIR, SCALE_FACTOR, TILE_SIZE
import lamp
import os, sys

class Target(lamp.GlowingSprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.kind = "target"
        self.glowing_radius = 100
        #self.glowing_color = (90, 90, 90)

        self.image = pygame.image.load(os.path.join(DATA_DIR, "exit", "exit.png")).convert()
        rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (rect.width * SCALE_FACTOR, rect.height * SCALE_FACTOR))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (x + TILE_SIZE//2, y + TILE_SIZE) 




