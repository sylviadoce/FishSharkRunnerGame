# Shark class
# Benjamin Antupit

import math
from random import shuffle


class Shark:

    def __init__(self):
        self.position = [7, 2, 0]
        self.max_distance = 2.49  # Max direct distance

    def getNextPosition(self, fish_pos: list) -> list:
        distances = []
        for pos in fish_pos:
            distances.append(math.dist(pos[:2], self.position[:2]))
        shuffle(distances)
        fish_distance = min(distances)
        closest_fish = fish_pos[distances.index(fish_distance)]
        delta_position = [
            round(min(self.max_distance, fish_distance) * (
                (closest_fish[0] - self.position[0]) / fish_distance)),
            round(min(self.max_distance, fish_distance) * (
                (closest_fish[1] - self.position[1]) / fish_distance))]
        self.position = [self.position[0] + delta_position[0],
                         self.position[1] + delta_position[1],
                         math.degrees(math.atan2(
                             closest_fish[1] - self.position[1],
                             closest_fish[0] - self.position[0]))]
        return self.position


if __name__ == "__main__":
    shark = Shark()
    print(shark.position)
    print(shark.getNextPosition([[7, 1]]))
    print(shark.getNextPosition([[1, 1]]))
