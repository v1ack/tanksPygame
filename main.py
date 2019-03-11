import sys
from classes import *
from map_loader import open_map
from os import path

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

    def game(self):
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
            for i in sprites:
                i.kill()
            self.screen.fill((0, 0, 0))
        text = "Press [ENTER] To Begin" if self.state == 'menu' else "Press [ENTER] To play again"
        draw_text(self.screen, text, 30, self.WIDTH / 2, self.HEIGHT / 2, self.font_name)
        pygame.display.flip()
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_RETURN]:
            self.state = 'game'
            open_map(path.join(assets_dir, 'map2'))

    def main(self):
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if self.state == 'game':
                self.game()
            if self.state == 'menu' or self.state == 'game_over':
                self.menu()


if __name__ == '__main__':
    tanki = Game()
    tanki.main()
