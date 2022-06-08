import os


EPSILON = 1e-12

PLAYER_COLOR = (255, 100, 100)
CAMERA_XBORDER = 250
CAMERA_YBORDER = 120


TILE_COLOR = (255, 255, 255)
DATA = os.path.join("data", "world.txt")
TILE_SIZE = 64

GROUND_DIR = os.path.join("data", "ground")
GROUND_TOP = os.path.join(GROUND_DIR, "ground_1.png")
GROUND_TOPLEFT = os.path.join(GROUND_DIR, "ground_2.png")
GROUND_LEFT = os.path.join(GROUND_DIR, "ground_3.png")
GROUND_BULK = os.path.join(GROUND_DIR, "ground_4.png")
GROUND_TOPLEFTRIGHT = os.path.join(GROUND_DIR, "ground_5.png")
GROUND_LEFTRIGHT = os.path.join(GROUND_DIR, "ground_6.png")


WINDOW_SIZE = (800, 600)