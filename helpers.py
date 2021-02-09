import pygame
from pygame.locals import *
import sys
import random
import math

def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.SysFont(textFont, textSize)
    newText=newFont.render(message, 0, textColor)

    return newText
