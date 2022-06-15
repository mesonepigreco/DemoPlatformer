import pygame
import pytest
import player, world

from Settings import *


pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)

clock = pygame.time.Clock()
pygame.mixer.init()

my_world = world.World()
my_world.create_world() 

running= True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    event = my_world.update(screen)
    if event == "Quit":
        running = False
    
    pygame.display.flip()
    