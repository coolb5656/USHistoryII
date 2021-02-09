import pygame
from pygame.locals import *
import sys
import random
import math

def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.SysFont(textFont, textSize)
    newText=newFont.render(message, 0, textColor)

    return newText

def load_question():
    f = open("questions.txt", "r")
    questions = []
    for x in f:
        z = x.strip()
        y = z.split(", ")
        questions.append(y)
    return questions[random.randrange(0, len(questions))]
