import sys
from classes import *
from map_loader import open_map

pygame.init()

WIDTH, HEIGHT = 800, 600


if __name__ == '__main__':
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TANKI")
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()
    enemes = pygame.sprite.Group()
    sprites_blocks, player, enemes = open_map('map1')
    sprites.add(player)
    # sprites_blocks.add(Bricks(100, 200), Bricks(32, 0), Bricks(64, 0))
    sprites.add(sprites_blocks)
    sprites.add(enemes)

    while True:
        for bullet in bullets:
            bullets_hit = pygame.sprite.spritecollide(bullet, sprites_blocks, False)
            if len(bullets_hit):
                bullet.kill()
                bullets_hit[0].shot()
        blocks_hit_list = pygame.sprite.spritecollide(player, sprites_blocks, False)
        player.move_available = {'up': True, 'down': True, 'left': True, 'right': True}
        if blocks_hit_list:
            for i in blocks_hit_list:
                if not (i.rect.x + 32 < player.rect.x or i.rect.x > player.rect.x + 32) \
                        and 16 < player.rect.y - i.rect.y <= 32:
                    player.move_available['up'] = False
                    player.rect.y += 32 - player.rect.y + i.rect.y
                if not (i.rect.x + 32 < player.rect.x or i.rect.x > player.rect.x + 32) \
                        and -16 > player.rect.y - i.rect.y >= -32:
                    player.move_available['down'] = False
                    player.rect.y -= player.rect.y - i.rect.y + 32
                if not (i.rect.y + 32 < player.rect.y or i.rect.y > player.rect.y + 32) \
                        and 16 < player.rect.x - i.rect.x <= 32:
                    player.move_available['left'] = False
                    player.rect.x += 32 - player.rect.x + i.rect.x
                if not (i.rect.y + 32 < player.rect.y or i.rect.y > player.rect.y + 32) \
                        and -16 > player.rect.x - i.rect.x >= -32:
                    player.move_available['right'] = False
                    player.rect.x -= player.rect.x - i.rect.x + 32
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        sprites.add(bullets)
        screen.fill((0, 0, 0))
        sprites.draw(screen)
        sprites.update()
        pygame.display.flip()
