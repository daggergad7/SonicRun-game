import json
from operator import itemgetter

import pygame
from pygame import freetype

pygame.init()
BG_COLOR = pygame.Color('gray12')
BLUE = pygame.Color('dodgerblue')
FONT = freetype.Font(None, 24)


def save(highscores):
    with open('highscores.json', 'w') as file:
        json.dump(highscores, file)  # Write the list to the json file.


def load():
    try:
        with open('highscores.json', 'r') as file:
            highscores = json.load(file)  # Read the json file.
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist.
    # Sorted by the score.
    return sorted(highscores, key=itemgetter(1), reverse=True)





