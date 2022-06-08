import pygame
import player
import custom_group

from Settings import *


class World:
    def __init__(self):
        self.ground_top = pygame.image.load(GROUND_TOP).convert()
        self.ground_topleft = pygame.image.load(GROUND_TOPLEFT).convert_alpha()
        self.ground_left = pygame.image.load(GROUND_LEFT).convert()
        self.ground_bulk = pygame.image.load(GROUND_BULK).convert()
        self.ground_right = pygame.transform.flip(self.ground_left, True, False)
        self.ground_topright = pygame.transform.flip(self.ground_topleft, True, False)
        self.ground_leftright =  pygame.image.load(GROUND_LEFTRIGHT).convert()
        self.ground_topleftright =  pygame.image.load(GROUND_TOPLEFTRIGHT).convert_alpha()


        self.ground_top = pygame.transform.scale(self.ground_top, (TILE_SIZE, TILE_SIZE))
        self.ground_topleft = pygame.transform.scale(self.ground_topleft, (TILE_SIZE, TILE_SIZE))
        self.ground_left = pygame.transform.scale(self.ground_left, (TILE_SIZE, TILE_SIZE))
        self.ground_bulk = pygame.transform.scale(self.ground_bulk, (TILE_SIZE, TILE_SIZE))
        self.ground_right = pygame.transform.scale(self.ground_right, (TILE_SIZE, TILE_SIZE))
        self.ground_topright = pygame.transform.scale(self.ground_topright, (TILE_SIZE, TILE_SIZE))
        self.ground_leftright = pygame.transform.scale(self.ground_leftright, (TILE_SIZE, TILE_SIZE))
        self.ground_topleftright = pygame.transform.scale(self.ground_topleftright, (TILE_SIZE, TILE_SIZE))



        self.background = pygame.Surface(WINDOW_SIZE)
        self.background.fill((0,0,0))


        self.player = None
        self.tiles = []


        self.camera = pygame.math.Vector2(0,0)

        self.visible_group = custom_group.MyGroup(self.camera)
        self.collision_group = pygame.sprite.Group()

    def update(self, screen):
        # Update all 
        self.visible_group.update(self.collision_group)
        
        self.player.update_camera(self.camera, screen.get_width(), screen.get_height())
        #for sprite in self.visible_group.sprites():
        #    sprite.update_rect(self.camera)


        screen.blit(self.background, (0,0))
        self.visible_group.draw(screen)

    def update_tile_images(self):
        for tile in self.visible_group:
            if tile.kind != "tile":
                continue

            has_left = False
            has_right = False
            has_top = False

            for secondtile in self.visible_group:
                if secondtile.kind != "tile":
                    continue

                delta_x = tile.rect.x - secondtile.rect.x
                delta_y = tile.rect.y - secondtile.rect.y

                if abs(delta_x - TILE_SIZE) < EPSILON and abs(delta_y) < EPSILON:
                    has_left = True
                elif abs(delta_x + TILE_SIZE) < EPSILON and abs(delta_y) < EPSILON:
                    has_right = True
                
                if abs(delta_y  - TILE_SIZE) < EPSILON and abs(delta_x) < EPSILON:
                    has_top = True

                #print("TILE AT: {} AND {}: L:{} R:{} T:{}".format( (tile.x// TILE_SIZE, tile.y//TILE_SIZE),
                #    (secondtile.x// TILE_SIZE, secondtile.y//TILE_SIZE),
                #    has_left, has_right, has_top))

            
            
            if has_left and has_right and has_top:
                tile.image = self.ground_bulk
            elif has_left and has_top:
                tile.image = self.ground_right
            elif has_right and has_top:
                tile.image = self.ground_left
            elif has_left and not has_right and not has_top:
                tile.image = self.ground_topright
            elif has_right and not has_left and not has_top:
                tile.image = self.ground_topleft
            elif has_top and not has_left and not has_right:
                tile.image = self.ground_leftright
            elif not has_top and not has_left and not has_right:
                tile.image = self.ground_topleftright
            elif not has_top:
                tile.image = self.ground_top
            
            #else:
            #    tile.image = self.ground_bulk
                


    def create_world(self, data_file = DATA):
        with open(data_file, "r") as fp:
            for yindex, line in enumerate(fp.readlines()):
                for xindex, character in enumerate(line.strip()):
                    x = xindex * TILE_SIZE
                    y = yindex * TILE_SIZE

                    if character == "0":
                        continue
                    elif character == "1":
                        tile = Tile(x, y, self.visible_group, self.collision_group)
                    elif character == "P":
                        self.player = player.Player(x, y, self.visible_group)

        #if self.player is not None:
        #    self.visible_group.move_to_front(self.player)

        self.update_tile_images()



class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self._layer = 1
        self.kind = "tile"
        self.image = pygame.Surface((64, 64))
        self.image.fill(TILE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self, dumb = None):
        pass


