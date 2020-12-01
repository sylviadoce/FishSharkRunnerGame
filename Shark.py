# Shark class
# Benjamin Antupit

from random import randrange
import math

class Shark:
    def __init__(self):
        self.position = [7,2,0]

    def getNextPosition(self, fish_pos: list) -> list:
        return list

    def getClosestFish(self, fish_pos) -> list:
        distances = []
        for pos in fish_pos:
            distances.append(math.dist(pos[:2], self.position[:2]))
        return fish_pos[distances.index(min(distances))]

if __name__ == "__main__":
    shark = Shark()
    print(shark.getClosestFish([[1,2], [2,4], [7,6]]))
