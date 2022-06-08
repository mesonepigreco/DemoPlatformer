import pygame
from Modules.Settings import TILE_SIZE
import lamp

class Target(lamp.GlowingSprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.kind = "target"
        self.glowing_radius = 100
        self.glowing_color = (90, 90, 90)

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE*3 //2))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x + TILE_SIZE//2, y + TILE_SIZE) 



