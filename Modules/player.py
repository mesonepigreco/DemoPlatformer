import pygame
import os

from Settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.kind = "player"
        self._layer = 2

        #self.image = pygame.Surface((64, 64*2))
        #self.image.fill(PLAYER_COLOR)
        miner_img_path = os.path.join("data", "miner", "miner.png")
        self.image = pygame.image.load(miner_img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))


        self.facing_right_surface = self.image.copy()
        self.facing_left_surface = pygame.transform.flip(self.image, True, False)


        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.centery = y

        self.hitbox = self.rect.inflate(-20, 0)


        self.direction = pygame.math.Vector2(0,0)
        self.speed = 5
        self.max_vertical_speed = 5
        self.increase_vertical_direction = 0.3
        self.jump_speed = 5.6

        self.is_going_left = False
        self.is_going_right = False

        self.is_grounded = False



    def update_rect(self):
        self.rect.center = self.hitbox.center

    def update_image(self):
        if self.is_going_left:
            self.image = self.facing_left_surface
        elif self.is_going_right:
            self.image = self.facing_right_surface

    def update(self, collision_group):
        self.update_direction()

        self.update_image()

        self.hitbox.x += self.direction.x * self.speed
        self.detect_collistions(collision_group, left_right= True)
        self.hitbox.y += self.direction.y * self.speed
        self.detect_collistions(collision_group, left_right=False)


        self.update_rect()

        


    def update_camera(self, camera_origin, screen_width, screen_height):
        # Player specific stuff
        player_vector = pygame.math.Vector2(self.hitbox.x,self.hitbox.y) + pygame.math.Vector2(self.rect.width / 2, self.rect.height / 2)
        dist_vect = player_vector - camera_origin

        if self.kind == "player":
            if dist_vect.x > screen_width - CAMERA_XBORDER:
                camera_origin.x = player_vector.x - screen_width + CAMERA_XBORDER
            elif dist_vect.x < CAMERA_XBORDER:
                camera_origin.x = player_vector.x - CAMERA_XBORDER


            if dist_vect.y  > screen_height - CAMERA_YBORDER:
                camera_origin.y = player_vector.y - screen_height + CAMERA_YBORDER
            elif dist_vect.y < CAMERA_YBORDER:
                camera_origin.y = player_vector.y - CAMERA_YBORDER
        



    def detect_collistions(self, collision_group, left_right = True):
        
        is_colliding = False

        for sprite in collision_group.sprites():
            if sprite.rect.colliderect(self.hitbox):
                is_colliding = True

                if left_right:
                    if self.is_going_right:
                        self.hitbox.right = sprite.rect.left
                    elif self.is_going_left:
                        self.hitbox.left = sprite.rect.right
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                        self.is_grounded = True
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom 

                    self.direction.y = 0



        if not left_right:
            if not is_colliding:
                self.is_grounded = False


    def update_direction(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.is_going_left = True
            self.is_going_right= False
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.is_going_left = False
            self.is_going_right= True
        else:
            self.direction.x = 0
            self.is_going_left = False
            self.is_going_right= False


        if keys[pygame.K_SPACE]:
            if self.is_grounded:
                self.direction.y = -self.jump_speed
        


        
        self.direction.y += self.increase_vertical_direction
        if self.direction.y > self.max_vertical_speed:
            self.direction.y = self.max_vertical_speed


