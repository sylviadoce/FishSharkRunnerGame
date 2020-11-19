# Shark class
# Benjamin Antupit

from random import randrange

def __init__(self, init_pos: list):
    self.position = init_pos
    self.direction = randrange(0,3)

def getNextPosition(sharkPos: list, fishPos: list) -> list:
