import pygame
from pygame.locals import *
import sys
import random
import math

from helpers import *

pygame.init()
vec = pygame.math.Vector2

# Set vars all caps means constant and it should not change
HEIGHT = int(1080/2)

WIDTH = int(1920/2)
ACC = 1
FRIC = -0.12
FPS = 60

# Colors
WHITE=(255, 255, 255)
BLACK=(0, 0, 0)
GRAY=(50, 50, 50)
RED=(255, 0, 0)
GREEN=(0, 255, 0)
BLUE=(0, 0, 255)
YELLOW=(255, 255, 0)

FONT = 'pacifico'

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Race!")

bg = pygame.image.load("pics/bg.jpg").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("pics/US.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (64, 64))
        self.rect = self.surf.get_rect()

        self.pos = vec((250, HEIGHT - 100))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.health = 4
        self.score = 0

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

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.image.load("pics/rock.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (48,48))
        self.rect = self.surf.get_rect(center = (x, y))

    def move(self):
        pass

class Bernie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.image.load("pics/bernie.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (256, 128))
        self.rect = self.surf.get_rect(center = (x, y))

    def move(self):
        pass

# Main Menu
def start():
    menu=True
    selected="start"

    moon = pygame.sprite.Sprite

    moon.surf = pygame.image.load("pics/moon.png").convert_alpha()
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
                        menu = False
                        main()
                    if selected=="quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        bg = pygame.image.load("pics/bg.jpg").convert()
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))



        displaysurface.blit(bg, (0,0))
        title=text_format("Space Race", FONT, 90, YELLOW)
        if selected=="start":
            text_start=text_format("START", FONT, 75, WHITE)
        else:
            text_start = text_format("START", FONT, 75, BLACK)
        if selected=="quit":
            text_quit=text_format("QUIT", FONT, 75, WHITE)
        else:
            text_quit = text_format("QUIT", FONT, 75, BLACK)

        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()

        # Main Menu Text
        displaysurface.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        displaysurface.blit(text_start, (WIDTH/2 - (start_rect[2]/2), 300))
        displaysurface.blit(text_quit, (WIDTH/2 - (quit_rect[2]/2), 360))

        displaysurface.blit(moon.surf, (WIDTH/2 - (title_rect[2]/2), 80))

        pygame.display.update()
        FramePerSec.tick(FPS)

# starting the game
def main():
    P1 = Player()
    playing = True

    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)

    asteroids = pygame.sprite.Group()

    for x in range(1, 5):
        ast = Asteroid(random.randrange(0, WIDTH), random.randrange(0, HEIGHT / 3))
        asteroids.add(ast)
        all_sprites.add(ast)

    bernies = pygame.sprite.Group()

    rate = 3

    pygame.time.set_timer(101, 5000)

    while playing:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == 101:
                bern = Bernie(random.randrange(0, WIDTH), 50)
                bernies.add(bern)
                all_sprites.add(bern)
            if len(asteroids) < 7:
                    ast = Asteroid(random.randrange(0, WIDTH), 50)
                    asteroids.add(ast)
                    all_sprites.add(ast)

        if len(asteroids) < 10:
            ast = Asteroid(random.randrange(0, WIDTH), 50)
            asteroids.add(ast)
            all_sprites.add(ast)

        for ast in asteroids:
            ast.rect.y += rate
            if(pygame.sprite.collide_rect(ast, P1)):
                P1.health -= 1
                ast.kill()
            if(ast.rect.y > HEIGHT - 100):
                ast.kill()

        for bern in bernies:
            bern.rect.y += rate * .7
            if(pygame.sprite.collide_rect(bern, P1)):
                if(question("What is 2+2?", "4")):
                    P1.score += 100
                bern.kill()
            if(bern.rect.y > HEIGHT - 100):
                bern.kill()

        if P1.health < 0:
            playing = False
            game_over()


        text_health=text_format("Health:" + str(P1.health + 1), FONT, 48, WHITE)
        text_score=text_format("Score:" + str(P1.score), FONT, 48, WHITE)

        displaysurface.blit(bg, (0,0))
        for ent in all_sprites:
            displaysurface.blit(ent.surf, ent.rect)
            ent.move()
        displaysurface.blit(text_health, (0,0))
        displaysurface.blit(text_score, (0,50))

        pygame.display.update()
        FramePerSec.tick(FPS)

# game over screen
def game_over():
    menu=True
    selected="start"

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
                        menu = False
                        main()

                    if selected=="quit":
                        pygame.quit()
                        quit()

        bg = pygame.image.load("pics/bg.jpg").convert()
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))



        displaysurface.blit(bg, (0,0))
        title=text_format("GAME OVER!", FONT, 90, YELLOW)
        if selected=="start":
            text_start=text_format("RESTART", FONT, 75, WHITE)
        else:
            text_start = text_format("RESTART", FONT, 75, BLACK)
        if selected=="quit":
            text_quit=text_format("QUIT", FONT, 75, WHITE)
        else:
            text_quit = text_format("QUIT", FONT, 75, BLACK)

        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()

        displaysurface.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        displaysurface.blit(text_start, (WIDTH/2 - (start_rect[2]/2), 300))
        displaysurface.blit(text_quit, (WIDTH/2 - (quit_rect[2]/2), 360))

        pygame.display.update()
        FramePerSec.tick(FPS)

# question
def question(q, answer):
    question=True

    text = ''

    font = pygame.font.SysFont(FONT, 48)
    text_box = font.render(text, True, RED)
    text_box_rect = text_box.get_rect()

    while question:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if len(text)>0:
                        text = text[:-1]
                elif event.key == K_RETURN:
                    question = False
                    return text == answer
                else:
                    text += event.unicode
                text_box = font.render(text, True, RED)
                text_box_rect.size=text_box.get_size()


        # Main Menu UI
        bg = pygame.image.load("pics/bg.jpg").convert()
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))



        displaysurface.blit(bg, (0,0))
        title=text_format(q, FONT, 90, YELLOW)
        title_rect=title.get_rect()



        # Main Menu Text
        displaysurface.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        displaysurface.blit(text_box, (WIDTH/2 - (title_rect[2]/2), 250))


        pygame.display.update()
        FramePerSec.tick(FPS)

start()
