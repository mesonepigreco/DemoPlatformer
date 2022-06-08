import pygame
from Settings import *

class GlowingSprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.glowing_color = (50, 40, 40)
        self.glowing_radius = 80
        self._layer = 0

    def get_glowing_surface(self):
        surface = pygame.Surface( (self.glowing_radius*2, self.glowing_radius*2))
        pygame.draw.circle(surface, self.glowing_color, (self.glowing_radius, self.glowing_radius), self.glowing_radius)
        surface.set_colorkey((0,0,0))

        return surface

        

class Lamp(GlowingSprite):

    def __init__(self, x, y, *groups):
        super().__init__(*groups)   
        self.kind = "lamp"
        self.image = pygame.Surface((TILE_SIZE//2, TILE_SIZE//2))
        self.image.fill((250, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x + TILE_SIZE // 2, y + TILE_SIZE)

        self.oil = 50

        self.glowing_color = (40, 30, 30)
        self.glowing_radius = self.oil * RADIUS_OIL_SCALE



