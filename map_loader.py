# import pygame
from classes import *


def open_map(map_name):
    with open(map_name, 'r') as map_file:
        map_size = list(map(int, map_file.readline()[:-1].split('x')))
        # map_content = map_file.read()
        map_struct = [i.split(',') for i in map_file.read().replace('\n', '').split(';')]
        # print(map_struct)
        game_map = pygame.sprite.Group()
        enemes = pygame.sprite.Group()
        player = None
        for i in range(map_size[0]):
            for j in range(map_size[1]):
                if map_struct[i][j] == 'i':
                    game_map.add(Iron(j * 32, i * 32))
                if map_struct[i][j] == 'b':
                    game_map.add(Bricks(j * 32, i * 32))
                if map_struct[i][j] == 'p':
                    player = PlayerTank(j * 32, i * 32)
                if map_struct[i][j] == 'e':
                    enemes.add(TankEnemy(j * 32, i * 32))
        return game_map, player, enemes

# open_map('map0')
