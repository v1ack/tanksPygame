import sys
from classes import *
from map_loader import open_map
from os import path

pygame.init()

if __name__ == '__main__':
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("TANKI")
    clock = pygame.time.Clock()
    open_map(path.join(assets_dir, 'map2'))

    while True:
        clock.tick(30)
        for bullet in bullets_group:
            bullets_hit = pygame.sprite.spritecollide(bullet, blocks_group, False)
            if len(bullets_hit):
                bullet.kill()
                bullets_hit[0].shot()
            bullets_hit_tanks = pygame.sprite.spritecollide(bullet, tanks_group, False)
            if len(bullets_hit_tanks) and pygame.time.get_ticks() - bullet.appear > 100:
                bullet.kill()
                bullets_hit_tanks[0].get_shot()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))
        sprites.draw(screen)
        sprites.update()
        pygame.display.flip()
