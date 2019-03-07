from classes import *


def open_map(map_name):
    with open(map_name, 'r') as map_file:
        map_size = list(map(int, map_file.readline()[:-1].split('x')))
        map_struct = [i.split(',') for i in map_file.read().replace('\n', '').split(';')]
        player = None
        for i in range(map_size[0]):
            for j in range(map_size[1]):
                if map_struct[i][j] == 'i':
                    Iron(j * 32, i * 32)
                if map_struct[i][j] == 'b':
                    Bricks(j * 32, i * 32)
                if map_struct[i][j] == 'p':
                    player = PlayerTank(j * 32, i * 32)
                if map_struct[i][j] == 'e':
                    TankEnemy(j * 32, i * 32)
        return player
