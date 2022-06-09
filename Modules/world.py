import pygame
import player
import custom_group, lamp, target

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


        # Background properties
        self.background = pygame.image.load(os.path.join(DATA_DIR, "background", "background.png")).convert()
        new_dim = [self.background.get_rect().width * SCALE_FACTOR,
            self.background.get_rect().height * SCALE_FACTOR]
        self.background = pygame.transform.scale(self.background, new_dim)
        self.distance_factor = 0.2


        self.darkness = pygame.Surface(WINDOW_SIZE)
        self.darkness.fill((50, 50, 50))

        # The font properties
        self.font_small = pygame.font.Font(FONT_LOCATION, FONT_SIZE_SMALL)
        self.font_title = pygame.font.Font(FONT_LOCATION, FONT_SIZE_TITLE)
        

        self.player = None
        self.tiles = []


        self.camera = pygame.math.Vector2(0,0)

        self.visible_group = custom_group.MyGroup(self.camera)
        self.collision_group = pygame.sprite.Group()
        self.glowing_group = pygame.sprite.Group()
        self.collectable_group = pygame.sprite.Group()

        # General info
        self.pause = False
        self.level = 0
        

    def background_blit(self, screen):
        origin = -self.camera * self.distance_factor
        
        screen_width = screen.get_rect().width
        screen_height = screen.get_rect().height

        background_width = self.background.get_rect().width
        background_height = self.background.get_rect().height


        origin.x = origin.x % background_width - background_width
        origin.y = origin.y % background_height - background_height


        start_x = origin.x
        while start_x < screen_width:
            start_y = origin.y
            while start_y < screen_width:
                screen.blit(self.background, (start_x, start_y))
                start_y += background_height
            start_x += background_width


    def check_death(self):
        if self.player.remaining_oil <= 0:
            return True
        return False

    def blit_text_on_center(self, text, surface, below = None, offset = 50):

        text_surface = self.font_title.render(text, False, (255, 255, 255), (0,0,0))
        text_surface.set_colorkey((0,0,0))

        text_rect = text_surface.get_rect()
        screen_rect = surface.get_rect()

        text_rect.center = screen_rect.center

        if below is not None:
            text_rect.midtop = below.midbottom
            text_rect.y += offset


        surface.blit(text_surface, text_rect)
        return text_rect


    def update(self, screen):
        # Update all 

        if not self.pause:
            self.visible_group.update(self.collision_group)
        
        self.player.update_camera(self.camera, screen.get_width(), screen.get_height())
        self.player.update_collectable(self.collectable_group)
        #for sprite in self.visible_group.sprites():
        #    sprite.update_rect(self.camera)

        self.background_blit(screen)
        self.visible_group.draw(screen)

        # Add the darkness
        self.update_glowing(screen)

        # Check death
        if self.check_death():
            self.pause = True
            t1 = self.blit_text_on_center("The moster of darkness got you!", screen)
            t2 = self.blit_text_on_center("Press enter to restart...", screen, below = t1)


    def start_level(self, level_file):
        # Reset the group
        self.glowing_group.empty()
        self.collectable_group.empty()
        self.visible_group.empty()
        self.collectable_group.empty()

        self.player = None

        self.create_world(level_file)




    def update_glowing(self, screen):
        
        # Add the glowing around all the sprites inside the glowing group
        new_darkness = self.darkness.copy()
        for sprite in self.glowing_group.sprites():
            glowing_surface = sprite.get_glowing_surface()
            glowing_rect = glowing_surface.get_rect()
            pos = list(sprite.rect.center)
            pos[0] -= glowing_rect.width / 2 
            pos[1] -= glowing_rect.height / 2

            pos[0] -= self.camera.x
            pos[1] -= self.camera.y

            new_darkness.blit(glowing_surface, pos,  special_flags = pygame.BLEND_SUB)

        screen.blit(new_darkness, (0,0), special_flags = pygame.BLEND_SUB)
        #screen.blit(glowing_surface, pos, special_flags = pygame.BLEND_ADD)

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
                


    def create_world(self, data_file = DATA_WORLD, offset_tiles = 5):
        maxx = 0
        maxy = 0
        with open(data_file, "r") as fp:
            for yindex, line in enumerate(fp.readlines()):
                for xindex, character in enumerate(line.strip()):
                    x = xindex * TILE_SIZE
                    y = yindex * TILE_SIZE

                    if x > maxx:
                        maxx = x
                    if y > maxy: 
                        maxy = y

                    if character == "0":
                        continue
                    elif character == "1":
                        Tile(x, y, self.visible_group, self.collision_group)
                    elif character == "P":
                        self.player = player.Player(x, y, self.visible_group, self.glowing_group)
                    elif character == "L":
                        lamp.Lamp(x, y, self.visible_group, self.glowing_group, self.collectable_group)
                    elif character == "T":
                        target.Target(x, y, self.visible_group, self.glowing_group, self.collectable_group)

        #if self.player is not None:
        #    self.visible_group.move_to_front(self.player)

        # Fill the border with tiles
        for x in range(offset_tiles):
            for y in range(offset_tiles):
                # Create the tiles in the corners
                Tile(-(x+1) * TILE_SIZE, -(y+1) * TILE_SIZE, self.visible_group, self.collision_group)
                Tile(maxx + x * TILE_SIZE, -(y+1) * TILE_SIZE, self.visible_group, self.collision_group)
                Tile(-(x+1) * TILE_SIZE, maxy +y * TILE_SIZE, self.visible_group, self.collision_group)
                Tile(maxx + x * TILE_SIZE, maxy + y * TILE_SIZE, self.visible_group, self.collision_group)

        
        for x in range(offset_tiles):
            for y in range(maxy // TILE_SIZE):
                Tile(-(x+1) * TILE_SIZE, y * TILE_SIZE, self.visible_group, self.collision_group)
                Tile(maxx+ x * TILE_SIZE, y * TILE_SIZE, self.visible_group, self.collision_group)

        for y in range(offset_tiles):
            for x in range(maxx // TILE_SIZE):
                Tile(x * TILE_SIZE, -(y+1) * TILE_SIZE, self.visible_group, self.collision_group)
                Tile(x * TILE_SIZE, maxy + y * TILE_SIZE, self.visible_group, self.collision_group)


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


