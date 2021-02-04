import pygame
from pygame.locals import *
import sys
import random
import math

pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional

HEIGHT = 1080
WIDTH = 1920
ACC = 0.5
FRIC = -0.02
FPS = 60

MAX_RATE = 10
GROWTH_RATE = .02

FramePerSec = pygame.time.Clock()


displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

bg = pygame.image.load("pics/bg.jpg").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("pics/US.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (64, 64))
        self.rect = self.surf.get_rect()

        self.pos = vec((250, HEIGHT - 250))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False

    def move(self):
        self.acc = vec(0,0)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("pics/soviet.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (64, 64))
        self.rect = self.surf.get_rect()

        self.pos = vec((WIDTH - 250, HEIGHT - 250))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False

    def move(self):
        self.acc = vec(0,0)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_d]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False


class platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.image.load("pics/rock.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (64, 64))
        self.rect = self.surf.get_rect(center = (x, y))

    def move(self):
        pass


def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False

P1 = Player()
P2 = Player2()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(P2)

platforms = pygame.sprite.Group()



rate = 1

pygame.time.set_timer(100, 250)

while True:
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == 100:
            pl = platform(random.randrange(0, WIDTH), 50)
            platforms.add(pl)
            all_sprites.add(pl)
            pl = platform(random.randrange(0, WIDTH), 50)
            platforms.add(pl)
            all_sprites.add(pl)

        if rate < MAX_RATE:
            rate += rate * GROWTH_RATE

    for plat in platforms:
        plat.rect.y += rate

    displaysurface.blit(bg, (0,0))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

    pygame.display.update()
    FramePerSec.tick(FPS)
