import pygame
from Settings import *
import math

class GlowingSprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.nonlinar_drop = 0.3
        self.n_stages = 50
        self.glowing_color = (255, 230, 230)
        self.glowing_radius = 80
        self._layer = 0

    def brightness_function(self, r, color_index):
        if self.glowing_radius == 0:
            x = 0
        else:      
            x = r / self.glowing_radius

        # liner
        #return self.glowing_color[color_index] * 

        linear_factor = 1 - x
        sqrt_factor = math.sqrt(1 - x)

        total_factor = (1-self.nonlinar_drop)*linear_factor + self.nonlinar_drop * sqrt_factor
        return self.glowing_color[color_index] * total_factor




    def get_glowing_surface(self):
        surface = pygame.Surface( (self.glowing_radius*2, self.glowing_radius*2))

        r = self.glowing_radius
        dr = r / self.n_stages
        for i in range(self.n_stages):
            color = [ self.brightness_function(r, 0),
                self.brightness_function(r, 1),
                self.brightness_function(r, 2)]
            pygame.draw.circle(surface, color, (self.glowing_radius, self.glowing_radius), r)
            r -= dr
        surface.set_colorkey((0,0,0))

        return surface

        

class Lamp(GlowingSprite):

    def __init__(self, x, y, *groups):
        super().__init__(*groups)   
        self.kind = "lamp"

        self.animation_speed = 0.4

        self.current_frame = 0
        self.frames = []
        for i in range(7):
            surface = pygame.image.load(os.path.join(DATA_DIR, "lamp", "lamp{:04d}.png".format(i))).convert_alpha()
            rect = surface.get_rect()
            surface = pygame.transform.scale(surface, (rect.width * SCALE_FACTOR, rect.height * SCALE_FACTOR))
            self.frames.append(surface)

        self.rect = self.frames[0].get_rect()
        self.rect.midbottom = (x + TILE_SIZE // 2, y + TILE_SIZE)

        self.oil = 50

        #self.glowing_color = (40, 30, 30)
        self.glowing_radius = self.oil * RADIUS_OIL_SCALE

    def update(self, dumb = None):
        self.current_frame += self.animation_speed

        frame_index = int(self.current_frame) % len(self.frames)
        self.image = self.frames[frame_index]




