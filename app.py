import pygame
from pygame.locals import *
import sys
import random
import math


pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional

HEIGHT = int(1080/2)
WIDTH = int(1920/2)
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

# Colors
white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)

def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.SysFont(textFont, textSize)
    newText=newFont.render(message, 0, textColor)

    return newText

font = 'pacifico'

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("pics/US.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (64, 64))
        self.rect = self.surf.get_rect()

        self.pos = vec((250, HEIGHT - 100))
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
        hits = pygame.sprite.spritecollide(self, platforms, False)
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

        self.pos = vec((WIDTH - 250, HEIGHT - 100))
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
        hits = pygame.sprite.spritecollide(self, platforms, False)
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

class bernie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.image.load("pics/bernie.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (256, 128))
        self.rect = self.surf.get_rect(center = (x, y))

    def move(self):
        pass


P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)

platforms = pygame.sprite.Group()
bernies = pygame.sprite.Group()

def main():
    rate = 1

    pygame.time.set_timer(100, 250)
    pygame.time.set_timer(101, 5000)

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
            if event.type == 101:
                bern = bernie(random.randrange(0, WIDTH), 50)
                platforms.add(bern)
                all_sprites.add(bern)


            if rate < MAX_RATE:
                rate += rate * GROWTH_RATE

        P1.update()

        for plat in platforms:
            plat.rect.y += rate
            if(pygame.sprite.collide_rect(plat, P1)):
                fail()

        displaysurface.blit(bg, (0,0))
        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
            entity.move()

        pygame.display.update()
        FramePerSec.tick(FPS)

def fail():

    menu=True
    selected="start"

    moon = pygame.sprite.Sprite

    moon.surf = pygame.image.load("pics/moon_PNG36.png").convert_alpha()
    moon.surf = pygame.transform.scale(moon.surf, (20, 20))
    moon.rect = moon.surf.get_rect()

    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        main()

                    if selected=="quit":
                        pygame.quit()
                        quit()

        # Main Menu UI

        bg = pygame.image.load("pics/bg.jpg").convert()
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))



        displaysurface.blit(bg, (0,0))
        title=text_format("Space Race", font, 90, yellow)
        if selected=="start":
            text_start=text_format("Back To Main Menu", font, 75, white)
        else:
            text_start = text_format("START", font, 75, black)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 75, white)
        else:
            text_quit = text_format("QUIT", font, 75, black)

        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()

        # Main Menu Text
        displaysurface.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        displaysurface.blit(text_start, (WIDTH/2 - (start_rect[2]/2), 300))
        displaysurface.blit(text_quit, (WIDTH/2 - (quit_rect[2]/2), 360))

        displaysurface.blit(moon.surf, (WIDTH/2 - (title_rect[2]/2), 80))

        pygame.display.update()
        pygame.display.set_caption("Space Race to Moon!")
