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
text_group = pygame.sprite.Group()
maps_list = pygame.sprite.Group()


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
        self.control = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
                        'shot': pygame.K_SPACE}

    def update(self):
        super().update()
        key_state = pygame.key.get_pressed()
        speed_x, speed_y = 0, 0
        if key_state[self.control['left']] and self.move_available['left']:
            speed_x = -self.speed
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction]['left'])
            self.direction = 'left'
        if key_state[self.control['right']] and self.move_available['right']:
            speed_x = self.speed
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction]['right'])
            self.direction = 'right'
        if key_state[self.control['up']] and self.move_available['up']:
            speed_y = -self.speed
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction]['up'])
            self.direction = 'up'
        if key_state[self.control['down']] and self.move_available['down']:
            speed_y = self.speed
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction]['down'])
            self.direction = 'down'
        elif key_state[self.control['shot']]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.cooldown:
                self.last_shot = now
                Bullet(self.rect.x + 10, self.rect.y + 10, self.direction)
        self.rect.x += speed_x
        self.rect.y += speed_y


class PlayerTank2(PlayerTank):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.control = self.control = {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d,
                                       'shot': pygame.K_q}


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


class Text(pygame.sprite.Sprite):
    def __init__(self, text, x, y, size=40, max_len=16, interval=5, center=[False, False], group=text_group):
        super().__init__(group)
        self.font = pygame.font.Font(path.join(assets_dir, 'PressStart2P-Regular.ttf'), size)
        text = self.divide_text(text, max_len)
        image_pieces = [self.font.render(i, False, (255, 255, 255)) for i in text]
        text_height = sum(
            [(index + 1) * (surface.get_height() + interval) for index, surface in enumerate(image_pieces)])
        text_width = max([surface.get_width() for surface in image_pieces])
        self.image = pygame.Surface((text_width, text_height))
        for index, surface in enumerate(image_pieces):
            self.image.blit(surface, (int((text_width - surface.get_width()) / 2) if center[1] else 0,
                                      index * (surface.get_height() + interval)))
        self.rect = self.image.get_rect()
        self.rect.x = int(center[0] - text_width) / 2 if center[0] else x
        self.rect.y = int(center[1] - text_height) / 2 if center[1] else y

    @staticmethod
    def divide_text(text, max_len):
        s = text.split(' ')
        n = ['']
        cur_s = 0
        i = 0
        while i < len(s):
            if not len(n[cur_s]):
                if len(s[i]) < max_len:
                    n[cur_s] = s[i]
                else:
                    while len(s[i]) > max_len:
                        n[cur_s] = s[i][:max_len]
                        n.append('')
                        cur_s += 1
                        s[i] = s[i][max_len:]
                    n[cur_s] = s[i]
            elif len(n[cur_s] + s[i]) < max_len:
                n[cur_s] = n[cur_s] + ' ' + s[i]
            else:
                cur_s += 1
                n.append('')
                i -= 1
            i += 1
        return n


class MapInMenu(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.path = path.join(assets_dir, 'maps/' + self.name)
        self.text = Text(self.name, 0, 400, size=20, center=[800, False], group=maps_list, max_len=30)
        self.image = self.text.image
        self.rect = self.image.get_rect()
        self.rect.x = self.text.rect.x
        self.rect.y = self.text.rect.y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
