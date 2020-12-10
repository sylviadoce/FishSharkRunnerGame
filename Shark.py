# Shark class
# Benjamin Antupit

import math
from random import shuffle


class Shark:

    def __init__(self):
        self.position = [7, 2, 0]
        self.max_distance = 2.49  # Max direct distance
        self.following_fish = -1

    def getStalemate(self):
        return False

    def getPosition(self):
        return self.position[:2]

    def getNextPosition(self, fish_pos: list) -> list:
        distances = []
        for pos in fish_pos:
            distances.append(math.dist(pos[:2], self.position[:2]))

        if ((sorted(distances)[0] == sorted(distances)[1] and
             0 <= self.following_fish <= 1) or
            (sorted(distances)[0] == sorted(distances)[2])
                and self.following_fish > 0):
            closest_fish = fish_pos[self.following_fish]
        else:
            shuffle(distances)
            self.following_fish = distances.index(min(distances))
            closest_fish = fish_pos[self.following_fish]
        fish_distance = math.dist(closest_fish[:2], self.position[:2])
        if fish_distance > 0.4:
            self.position = [self.position[0] + round(
                        min(self.max_distance, fish_distance) * (
                            (closest_fish[0] - self.position[0])
                            / fish_distance)),
                             self.position[1] + round(
                        min(self.max_distance, fish_distance) * (
                            (closest_fish[1] - self.position[1])
                            / fish_distance))]
        print("shark follow", self.following_fish, "dist", fish_distance)
        return self.position


if __name__ == "__main__":
    shark = Shark()
    print(shark.position)
    print(shark.getNextPosition([[1, 1], [1, 2], [1, 3]]))
    print(shark.getNextPosition([[2, 1], [2, 2], [2, 3]]))
