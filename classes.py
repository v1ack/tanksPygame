import pygame
import random
from os import path

assets_dir = path.join(path.dirname(__file__), 'assets')

clock = pygame.time.Clock()
bullets_group = pygame.sprite.Group()
tanks_group = pygame.sprite.Group()
tanks_enemies = pygame.sprite.Group()
blocks_group = pygame.sprite.Group()
sprites = pygame.sprite.Group()
player = pygame.sprite.Group()


class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(blocks_group, sprites)
        self.image = None
        self.hp = None

    def shot(self, damage=1):
        if self.hp is not None:
            self.hp -= damage
            if self.hp < 1:
                self.kill()


class Bricks(Block):
    def __init__(self, x, y):
        super().__init__()
        self.hp = 1
        self.image = pygame.image.load(path.join(assets_dir, 'bricks.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Iron(Block):
    def __init__(self, x, y):
        super().__init__()
        self.hp = 100
        self.image = pygame.image.load(path.join(assets_dir, 'iron.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(tanks_group, sprites, groups)
        self.image = pygame.image.load(path.join(assets_dir, 'tank_c.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 2
        self.speed = 1
        self.move_available = {'up': True, 'down': True, 'left': True, 'right': True}
        self.move_available_last = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
        self.move_cooldown = 500
        self.direction = 'up'
        self.directions = {'left': {'up': 270, 'right': 180, 'down': 90, 'left': 0},
                           'right': {'up': 90, 'right': 0, 'down': 270, 'left': 180},
                           'up': {'up': 0, 'right': 270, 'down': 180, 'left': 90},
                           'down': {'up': 180, 'right': 90, 'down': 0, 'left': 270}}
        self.last_shot = 0
        self.cooldown = 500

    def update(self):
        now = pygame.time.get_ticks()
        blocks_hit_list = pygame.sprite.spritecollide(self, blocks_group, False)
        if blocks_hit_list:
            for i in blocks_hit_list:
                if not (i.rect.x + 32 < self.rect.x or i.rect.x > self.rect.x + 32) \
                        and 16 < self.rect.y - i.rect.y <= 32:
                    self.move_available_last['up'] = now
                    self.rect.y += 32 - self.rect.y + i.rect.y
                if not (i.rect.x + 32 < self.rect.x or i.rect.x > self.rect.x + 32) \
                        and -16 > self.rect.y - i.rect.y >= -32:
                    self.move_available_last['down'] = now
                    self.rect.y -= self.rect.y - i.rect.y + 32
                if not (i.rect.y + 32 < self.rect.y or i.rect.y > self.rect.y + 32) \
                        and 16 < self.rect.x - i.rect.x <= 32:
                    self.move_available_last['left'] = now
                    self.rect.x += 32 - self.rect.x + i.rect.x
                if not (i.rect.y + 32 < self.rect.y or i.rect.y > self.rect.y + 32) \
                        and -16 > self.rect.x - i.rect.x >= -32:
                    self.move_available_last['right'] = now
                    self.rect.x -= self.rect.x - i.rect.x + 32

        self.move_available = {i: True if now - self.move_available_last[i] > self.move_cooldown else False for i in
                               self.move_available.keys()}

    def get_shot(self):
        self.hp -= 1
        if self.hp <= 0:
            self.kill()


class TankEnemy(Tank):
    def __init__(self, x, y):
        super().__init__(x, y, tanks_enemies)
        self.speed = random.randrange(5, 10)

    def update(self):
        super().update()
        variants = ['left', 'right', 'up', 'down', 'space']
        random.shuffle(variants)
        key_state = variants[0]
        speed_x, speed_y = 0, 0
        if key_state == 'left' and self.move_available['left']:
            speed_x = -self.speed
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction]['left'])
            self.direction = 'left'
        elif key_state == 'right' and self.move_available['right']:
            speed_x = self.speed
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction]['right'])
            self.direction = 'right'
        elif key_state == 'up' and self.move_available['up']:
            speed_y = -self.speed
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction]['up'])
            self.direction = 'up'
        elif key_state == 'down' and self.move_available['down']:
            speed_y = self.speed
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction]['down'])
            self.direction = 'down'
        elif key_state == 'space':
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.cooldown:
                self.last_shot = now
                Bullet(self.rect.x + 10, self.rect.y + 10, self.direction)
        self.rect.x += speed_x
        self.rect.y += speed_y


class PlayerTank(Tank):
    def __init__(self, x, y):
        super().__init__(x, y, player)
        self.image = pygame.image.load(path.join(assets_dir, 'tank_p.png'))
        self.hp = 3
        self.speed = 10
        self.cooldown = 500

    def update(self):
        super().update()
        key_state = pygame.key.get_pressed()
        speed_x, speed_y = 0, 0
        if key_state[pygame.K_LEFT] and self.move_available['left']:
            speed_x = -self.speed
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction]['left'])
            self.direction = 'left'
        if key_state[pygame.K_RIGHT] and self.move_available['right']:
            speed_x = self.speed
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction]['right'])
            self.direction = 'right'
        if key_state[pygame.K_UP] and self.move_available['up']:
            speed_y = -self.speed
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction]['up'])
            self.direction = 'up'
        if key_state[pygame.K_DOWN] and self.move_available['down']:
            speed_y = self.speed
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction]['down'])
            self.direction = 'down'
        elif key_state[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.cooldown:
                self.last_shot = now
                Bullet(self.rect.x + 10, self.rect.y + 10, self.direction)
        self.rect.x += speed_x
        self.rect.y += speed_y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__(bullets_group, sprites)
        self.image = pygame.image.load(path.join(assets_dir, 'bullet2.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 15
        self.direction = direction
        self.appear = pygame.time.get_ticks()

    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
