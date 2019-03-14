from classes import *


def open_map(map_name):
    with open(map_name, 'r') as map_file:
        map_size = list(map(int, map_file.readline()[:-1].split('x')))
        map_structure = [i.split(',') for i in map_file.read().replace('\n', '').split(';')]
        for i in range(map_size[1]):
            for j in range(map_size[0]):
                if map_structure[i][j] == 'i':
                    Iron(j * 32, i * 32)
                if map_structure[i][j] == 'b':
                    Bricks(j * 32, i * 32)
                if map_structure[i][j] == 'p':
                    PlayerTank(j * 32, i * 32)
                if map_structure[i][j] == 'p2':
                    PlayerTank2(j * 32, i * 32)
                if map_structure[i][j] == 'e':
                    TankEnemy(j * 32, i * 32)
