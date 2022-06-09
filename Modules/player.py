import pygame
import os

from Settings import *
import lamp
class Player(lamp.GlowingSprite):

    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.kind = "player"
        self._layer = 2

        # Properties
        self.remaining_oil = 100
        self.drop_oil_rate = 0.2


        #self.image = pygame.Surface((64, 64*2))
        #self.image.fill(PLAYER_COLOR)
        miner_img_path = os.path.join("data", "miner", "miner.png")
        self.image = pygame.image.load(miner_img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))


        self.facing_right_surface = self.image.copy()
        self.facing_left_surface = pygame.transform.flip(self.image, True, False)


        # Load animations
        self.animations = {
            "fall_left" : [self.facing_left_surface],
            "fall_right" : [self.facing_right_surface]}

        self.load_animations( os.path.join(PLAYER_ANIMATION_DATA, "walk"), "walk_right", "walk", 6, flip = False)
        self.load_animations( os.path.join(PLAYER_ANIMATION_DATA, "walk"), "walk_left", "walk", 6, flip = True)
        self.load_animations( os.path.join(PLAYER_ANIMATION_DATA, "idle"), "idle_right", "idle", 13, 6, False)
        self.load_animations( os.path.join(PLAYER_ANIMATION_DATA, "idle"), "idle_left", "idle", 13, 6, True)
        self.load_animations( os.path.join(PLAYER_ANIMATION_DATA, "fall"), "fall_right", "fall", 18, 13, False)
        self.load_animations( os.path.join(PLAYER_ANIMATION_DATA, "fall"), "fall_left", "fall", 18, 13, True)

        self.status = "idle"
        self.current_frame = 0

        self.animation_speed = {"idle" : 0.1, "walk" : 0.25, "fall" : 0.14}


        # Hitbox and rect
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.hitbox = self.rect.inflate(-20, 0)

        # Moovment
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 5
        self.max_vertical_speed = 5
        self.increase_vertical_direction = 0.3
        self.jump_speed = 5.6

        self.is_going_left = False
        self.is_going_right = True
        self.is_grounded = False

        # Glowing
        #self.glowing_color = (50, 40, 40)
        self.glowing_radius = 150

    


    def load_animations(self, directory, animation_name, basename, end_frame, start_frame = 0, flip = False):
        frames = []
        for i in range(start_frame, end_frame):
            filename = os.path.join(directory, "{}{:04d}.png".format(basename, i))
            image = pygame.image.load(filename).convert_alpha()
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            if flip:
                image = pygame.transform.flip(image, True, False)
            frames.append(image)
        
        self.animations[animation_name] = frames
            



    def update_rect(self):
        self.rect.center = self.hitbox.center
    

    def update_status(self):
        if self.is_grounded:
            if abs(self.direction.x) > EPSILON:
                self.status = "walk"
            else:
                self.status = "idle"
        else:
            self.status = "fall" 


    def update_image(self):
        current_animation = self.status + "_"
        if self.is_going_left:
            current_animation += "left"
        elif self.is_going_right:
            current_animation += "right"
        
        # Update frames
        self.current_frame += self.animation_speed[self.status]

        animation = self.animations[current_animation]

        total_frames = len(animation)
        self.image = animation[int(self.current_frame) % total_frames]

    def update_oil(self):
        self.remaining_oil -= self.drop_oil_rate
        
        if self.remaining_oil < 0:
            self.remaining_oil = 0
        self.glowing_radius = self.remaining_oil * RADIUS_OIL_SCALE

    def update_collectable(self, collectable_group):
        for sprite in collectable_group.sprites():
            if sprite.rect.colliderect(self.hitbox):
                if sprite.kind == "lamp":
                    self.remaining_oil += sprite.oil
                    sprite.kill()


    def update(self, collision_group):
        self.update_direction()

        self.update_image()

        self.hitbox.x += self.direction.x * self.speed
        self.detect_collistions(collision_group, left_right= True)
        self.hitbox.y += self.direction.y * self.speed
        self.detect_collistions(collision_group, left_right=False)


        self.update_rect()
        self.update_oil()

        self.update_status()



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
            #self.is_going_left = False
            #self.is_going_right= False


        if keys[pygame.K_SPACE]:
            if self.is_grounded:
                self.direction.y = -self.jump_speed
        


        
        self.direction.y += self.increase_vertical_direction
        if self.direction.y > self.max_vertical_speed:
            self.direction.y = self.max_vertical_speed


