import pygame
import random

bullets = pygame.sprite.Group()


class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
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
        self.image = pygame.image.load('bricks.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Iron(Block):
    def __init__(self, x, y):
        super().__init__()
        self.hp = 100
        self.image = pygame.image.load('iron.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('tank_c.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 10
        self.speed = 1
        self.move_available = {'up': True, 'down': True, 'left': True, 'right': True}
        self.direction = 'up'
        self.directions = {'up': 0, 'right': 270, 'down': 180, 'left': 90}
        self.last_shot = 0
        self.cooldown = 500


class TankEnemy(Tank):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = random.randrange(5, 10)

    def update(self):
        variants = ['left', 'right', 'up', 'down', 'space']
        random.shuffle(variants)
        key_state = variants[0]
        speed_x, speed_y = 0, 0
        if key_state == 'left' and self.move_available['left']:
            speed_x = -self.speed
            self.direction = 'left'
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction])
            self.directions = {'up': 270, 'right': 180, 'down': 90, 'left': 0}
        elif key_state == 'right' and self.move_available['right']:
            speed_x = self.speed
            self.direction = 'right'
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction])
            self.directions = {'up': 90, 'right': 0, 'down': 270, 'left': 180}
        elif key_state == 'up' and self.move_available['up']:
            speed_y = -self.speed
            self.direction = 'up'
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction])
            self.directions = {'up': 0, 'right': 270, 'down': 180, 'left': 90}
        elif key_state == 'down' and self.move_available['down']:
            speed_y = self.speed
            self.direction = 'down'
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction])
            self.directions = {'up': 180, 'right': 90, 'down': 0, 'left': 270}
        elif key_state == 'space':
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.cooldown:
                self.last_shot = now
                bullets.add(Bullet(self.rect.x + 10, self.rect.y + 10, self.direction))
        self.rect.x += speed_x
        self.rect.y += speed_y


class PlayerTank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('tank_p.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = None
        self.speed = 10
        self.move_available = {'up': True, 'down': True, 'left': True, 'right': True}
        self.direction = 'up'
        self.directions = {'up': 0, 'right': 270, 'down': 180, 'left': 90}
        self.last_shot = 0
        self.cooldown = 500

    def update(self):
        key_state = pygame.key.get_pressed()
        speed_x, speed_y = 0, 0
        if key_state[pygame.K_LEFT] and self.move_available['left']:
            speed_x = -self.speed
            self.direction = 'left'
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction])
            self.directions = {'up': 270, 'right': 180, 'down': 90, 'left': 0}
        elif key_state[pygame.K_RIGHT] and self.move_available['right']:
            speed_x = self.speed
            self.direction = 'right'
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction])
            self.directions = {'up': 90, 'right': 0, 'down': 270, 'left': 180}
        elif key_state[pygame.K_UP] and self.move_available['up']:
            speed_y = -self.speed
            self.direction = 'up'
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction])
            self.directions = {'up': 0, 'right': 270, 'down': 180, 'left': 90}
        elif key_state[pygame.K_DOWN] and self.move_available['down']:
            speed_y = self.speed
            self.direction = 'down'
            self.image = pygame.transform.rotate(self.image, self.directions[self.direction])
            self.directions = {'up': 180, 'right': 90, 'down': 0, 'left': 270}
        elif key_state[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.cooldown:
                self.last_shot = now
                bullets.add(Bullet(self.rect.x + 10, self.rect.y + 10, self.direction))
        self.rect.x += speed_x
        self.rect.y += speed_y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.image.load('bullet2.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 15
        self.direction = direction

    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
