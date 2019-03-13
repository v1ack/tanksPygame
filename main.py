import sys
from classes import *
from map_loader import open_map
from os import path, listdir

pygame.init()


class Game:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("TANKI")
        self.clock = pygame.time.Clock()
        self.font_name = pygame.font.match_font('arial')
        self.state = 'menu'
        self.map_list = listdir(path.join(assets_dir, 'maps'))

    def game(self):
        while self.state == 'game':
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            for bullet in bullets_group:
                bullets_hit = pygame.sprite.spritecollide(bullet, blocks_group, False)
                if len(bullets_hit):
                    bullet.kill()
                    bullets_hit[0].shot()
                bullets_hit_tanks = pygame.sprite.spritecollide(bullet, tanks_group, False)
                if len(bullets_hit_tanks) and pygame.time.get_ticks() - bullet.appear > 100:
                    bullet.kill()
                    bullets_hit_tanks[0].get_shot()
            self.screen.fill((0, 0, 0))
            sprites.draw(self.screen)
            sprites.update()
            if len(tanks_group) <= 1:
                self.state = 'game_over'
            pygame.display.flip()

    def menu(self):
        if len(sprites):
            sprites.empty()
            self.screen.fill((0, 0, 0))
        if self.state == 'menu':
            Text('Press [ENTER] to begin a game', 0, 0, size=40, center=[self.WIDTH, self.HEIGHT])
        if self.state == 'game_over':
            Text('Press [ENTER] To play again', 0, 0, size=40, center=[self.WIDTH, self.HEIGHT])
        map_list = [MapInMenu(n) for n in listdir(path.join(assets_dir, 'maps'))]
        cur_map = 0
        while self.state == 'menu' or self.state == 'game_over':
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            map_list[cur_map].draw(self.screen)
            text_group.draw(self.screen)
            pygame.display.flip()
            key_state = pygame.key.get_pressed()
            if key_state[pygame.K_RETURN]:
                self.state = 'game'
                text_group.empty()
                open_map(map_list[cur_map].path)
            if key_state[pygame.K_RIGHT]:
                if cur_map < len(map_list) - 1:
                    cur_map += 1
                else:
                    cur_map = 0
            if key_state[pygame.K_LEFT]:
                if cur_map > 0:
                    cur_map -= 1
                else:
                    cur_map = len(map_list) - 1

    def main(self):
        while True:
            if self.state == 'game':
                self.game()
            if self.state == 'menu':
                self.menu()
            if self.state == 'game_over':
                self.menu()


if __name__ == '__main__':
    tanki = Game()
    tanki.main()
