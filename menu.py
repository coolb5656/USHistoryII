import pygame
from pygame.locals import *
import os

from app import main
    # Game Initialization
pygame.init()

# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Game Resolution
screen_width=int(1920/2)
screen_height=int(1080/2)
screen=pygame.display.set_mode((screen_width, screen_height))

# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.SysFont(textFont, textSize)
    newText=newFont.render(message, 0, textColor)

    return newText


# Colors
white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)

# Game Fonts
font = "pacifico"


# Game Framerate
clock = pygame.time.Clock()
FPS=60

# Main Menu
def main_menu():

    menu=True
    selected="start"

    moon = pygame.sprite.Sprite

    moon.surf = pygame.image.load("pics/moon_PNG36.png").convert_alpha()
    moon.surf = pygame.transform.scale(moon.surf, (100, 100))
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
                        pygame.quit()
                    if selected=="quit":
                        pygame.quit()
                        quit()

        # Main Menu UI

        bg = pygame.image.load("pics/bg.jpg").convert()
        bg = pygame.transform.scale(bg, (screen_width, screen_height))



        screen.blit(bg, (0,0))
        title=text_format("Space Race", font, 90, yellow)
        if selected=="start":
            text_start=text_format("START", font, 75, white)
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
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 360))

        screen.blit(moon.surf, (screen_width/2 - (title_rect[2]/2), 80))

        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Space Race to Moon!")

#Initialize the Game
main_menu()
