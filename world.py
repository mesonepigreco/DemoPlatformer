import pygame
import player
import custom_group, lamp, target, enemy
import ui
import menu
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

        # Menu 
        self.menu = menu.Menu(["Start game", "Load", "Save", "Quit"])
        self.display_menu = True

        self.loading_surface = pygame.Surface(WINDOW_SIZE)
        self.loading_surface.fill((0,0,0))
        text_surf = self.font_title.render("Loading level ...", False, (255, 255, 255), (0,0,0))
        text_rect = text_surf.get_rect()
        text_rect.center = (WINDOW_SIZE[0]//2, WINDOW_SIZE[1] // 2)
        self.loading_surface.blit(text_surf, text_rect)
        
        self.player = None
        self.tiles = []


        self.camera = pygame.math.Vector2(0,0)

        self.visible_group = custom_group.MyGroup(self.camera)
        self.collision_group = pygame.sprite.Group()
        self.glowing_group = pygame.sprite.Group()
        self.collectable_group = pygame.sprite.Group()
        self.winning_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.spawners = []

        # General info
        self.pause = False
        self.level = 0
        self.max_level = len([x for x in os.listdir(DATA_DIR) if x.startswith("level_") and x.endswith(".txt")])
        self.ui = ui.UserInterface(self.player, 0, self.font_small)

        # Music
        self.music = pygame.mixer.Sound(os.path.join(DATA_DIR, "main-theme.wav"))
        self.music.set_volume(0.1)
        #self.music.play(-1)

    def __setattr__(self, __name, __value):
        if __name == "player":
            if "ui" in self.__dict__:
                self.ui.player = __value   

        super().__setattr__(__name, __value)
        
    
    def save(self):
        with open(SAVE_FILE, "w") as fp:
            fp.write(str(self.level))


    def load(self):
        if not os.path.exists(SAVE_FILE):
            self.save()

        with open(SAVE_FILE, "r") as fp:
            self.level = int(fp.read().strip())

        self.start_level()

        

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

    def check_win(self):
        for sprite in self.winning_group.sprites():
            if sprite.rect.colliderect(self.player.hitbox):
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


    def check_enemy_collision(self):
        for sprite in self.enemy_group.sprites():
            if self.player.hitbox.colliderect(sprite.hitbox):
                self.player.push_back(sprite.push_back, sprite.direction.x - self.player.direction.x, 
                    sprite.steal_oil)

    def check_pause(self):
        keys = pygame.key.get_pressed()
        ticks = pygame.time.get_ticks()
        if (keys[pygame.K_RETURN]) and ticks - self.menu.check_return > self.menu.return_timeout:
            self.menu.check_return = ticks
            self.pause = True
            self.display_menu = True
            pygame.mixer.fadeout(400)
        if not keys[pygame.K_RETURN]:
            self.menu.check_return = 0

    def update(self, screen):
        # Update all 


        if not self.pause and not self.display_menu:
            self.check_pause()
            self.visible_group.update(self.collision_group)

            for spawner in self.spawners:
                spawner.update()
        
        
        self.check_enemy_collision()

        self.player.update_camera(self.camera, screen.get_width(), screen.get_height())
        self.player.update_collectable(self.collectable_group, self.ui)
        #for sprite in self.visible_group.sprites():
        #    sprite.update_rect(self.camera)

        self.background_blit(screen)
        self.visible_group.draw(screen)

        # Add the darkness
        self.update_glowing(screen)

        # Update the User Interface
        self.ui.draw(self.level)


        if self.display_menu:
            result = self.menu.update()
            if result is not None:
                if result == "Start game":
                    self.display_menu = False
                    self.pause = False

                    # Play again the music
                    self.music.play(-1)
                elif result == "Save":
                    self.save()

                    self.display_menu = False
                    self.pause = False

                    # Play again the music
                    self.music.play(-1)
                elif result == "Load":
                    self.display_menu = False
                    self.pause = False

                    # Play again the music
                    self.music.play(-1)
                    self.load()
                elif result == "Quit":
                    return "Quit"
            self.menu.draw(screen)

        # Check death
        if self.check_death():

            if self.pause == False:
                self.player.sound_death.play()
            self.pause = True

            t1 = self.blit_text_on_center("The moster of darkness got you!", screen)
            t2 = self.blit_text_on_center("Press enter to restart...", screen, below = t1)

            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.start_level()
                self.pause = False

        if self.check_win():

            if self.pause == False:
                self.level += 1
                self.player.sound_target.play()
            self.pause = True

            if self.level < self.max_level:
                t1 = self.blit_text_on_center("Huppy! We got an escape!", screen)
                t2 = self.blit_text_on_center("Press enter to continue...", screen, below = t1)
            else:
                # We finished the game
                t1 = self.blit_text_on_center("GAME COMPLETED!", screen)
                t2 = self.blit_text_on_center("Press enter to restart the game", screen, below = t1)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:

                if self.level == self.max_level:
                    self.level = 0
                self.start_level()
                self.pause = False


    def start_level(self):
        # Reset the group
        self.glowing_group.empty()
        self.collision_group.empty()
        self.visible_group.empty()
        self.collectable_group.empty()
        self.winning_group.empty()
        self.enemy_group.empty()

        self.player = None

        level_file = os.path.join(DATA_DIR, "level_{}.txt".format(self.level))
        
        screen = pygame.display.get_surface()
        screen.blit(self.loading_surface, (0,0))
        pygame.display.flip()
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

            new_darkness.blit(glowing_surface, pos,  special_flags = pygame.BLEND_ADD)

        screen.blit(new_darkness, (0,0), special_flags = pygame.BLEND_MULT)
        #screen.blit(glowing_surface, pos, special_flags = pygame.BLEND_ADD)

    def update_tile_images(self, maxx):
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

                if delta_x <= - 2*TILE_SIZE or delta_x >= 2*TILE_SIZE:
                    continue

                delta_y = tile.rect.y - secondtile.rect.y
                if delta_y <= - 2*TILE_SIZE or delta_y >= 2*TILE_SIZE:
                    continue

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

        total_lamps = 0
        with open(data_file, "r") as fp:
            for yindex, line in enumerate(fp.readlines()):
                for xindex, character in enumerate(line):
                    x = xindex * TILE_SIZE
                    y = yindex * TILE_SIZE

                    if x > maxx:
                        maxx = x
                    if y > maxy: 
                        maxy = y

                    if character == "1":
                        Tile(x, y, self.visible_group, self.collision_group)
                    elif character == "P":
                        self.player = player.Player(x, y, self.visible_group, self.glowing_group)
                    elif character == "L":
                        lamp.Lamp(x, y, self.visible_group, self.glowing_group, self.collectable_group)
                        total_lamps += 1
                    elif character == "T":
                        target.Target(x, y, self.visible_group, self.glowing_group, self.winning_group)
                    elif character == "S":
                        enemy.Slug(x, y, self.visible_group, self.enemy_group)
                    elif character == "O":
                        self.spawners.append(enemy.EnemySpawner(x, y, self.visible_group, self.enemy_group))
                    else:
                        continue

        #if self.player is not None:
        #    self.visible_group.move_to_front(self.player)

        # Fill the border with tiles
        for x in range(-1, offset_tiles):
            for y in range(offset_tiles):
                # Create the tiles in the corners
                Tile(-(x+1) * TILE_SIZE, -(y+1) * TILE_SIZE, self.visible_group, self.collision_group)
                Tile(maxx + (x+1) * TILE_SIZE, -(y+1) * TILE_SIZE, self.visible_group, self.collision_group)
                Tile(-(x+1) * TILE_SIZE, maxy +(y+1) * TILE_SIZE, self.visible_group, self.collision_group)
                Tile(maxx + (x + 1) * TILE_SIZE, maxy + (1 + y) * TILE_SIZE, self.visible_group, self.collision_group)

        
        for x in range( offset_tiles):
            for y in range(maxy // TILE_SIZE + 1):
                Tile(-(x+1) * TILE_SIZE, y * TILE_SIZE, self.visible_group, self.collision_group)
                Tile(maxx+ (x) * TILE_SIZE, y * TILE_SIZE, self.visible_group, self.collision_group)

        for y in range(offset_tiles):
            for x in range(maxx // TILE_SIZE):
                Tile(x * TILE_SIZE, -(y+1) * TILE_SIZE, self.visible_group, self.collision_group)
                Tile(x * TILE_SIZE, maxy + (1 + y) * TILE_SIZE, self.visible_group, self.collision_group)


        self.update_tile_images(maxx)

        self.ui.reset_counter(total_lamps)



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

        self.friction = 0.18


    def update(self, dumb = None):
        pass


