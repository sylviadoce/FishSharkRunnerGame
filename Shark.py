# Shark class
# Benjamin Antupit

import math
from random import sample


class Shark:

    def __init__(self):
        self.position = [7, 2, 0]
        self.max_distance = 2.49  # Max direct distance
        self.following_fish = -1
        self.previous_moves = [[], []]

    def getStalemate(self):
        if len(self.previous_moves[0]) >= 8:  # 8 moves have transpired
            print("shark x count", self.previous_moves[0].count(
                self.previous_moves[0][0]))
            print("shark y count", self.previous_moves[1].count(
                self.previous_moves[1][0]))
            return (self.previous_moves[0].count(
                self.previous_moves[0][0]) == len(self.previous_moves[0])
                    or self.previous_moves[1].count(
                self.previous_moves[1][0]) == len(self.previous_moves[1]))
        return False

    def getPosition(self):
        return self.position[:2]

    def getNextPosition(self, fish_pos: list) -> list:
        distances = []
        for pos in fish_pos:
            distances.append(math.dist(pos[:2], self.position[:2]))
        print("fish distances", distances, sorted(distances),
              min(distances), distances.index(min(distances)))

        if ((sorted(distances)[0] == sorted(distances)[1] and
             0 <= self.following_fish <= 1) or
            (sorted(distances)[0] == sorted(distances)[2])
                and self.following_fish > 0):
            closest_fish = fish_pos[self.following_fish]
            print("shark continue following fish", self.following_fish)
        else:
            self.following_fish = distances.index(
                min(sample(distances, 3)))
            closest_fish = fish_pos[self.following_fish]
            print("shark switch following fish", self.following_fish)
        fish_distance = math.dist(closest_fish[:2], self.position[:2])
        if fish_distance > 0.4:
            delta_position = [
                round(min(self.max_distance, fish_distance) * (
                    (closest_fish[0] - self.position[0]) / fish_distance)),
                round(min(self.max_distance, fish_distance) * (
                    (closest_fish[1] - self.position[1]) / fish_distance))]
            off_axis = [closest_fish[0] - self.position[0],
                        closest_fish[1] - self.position[1]]
            print("shark pre off axis", delta_position, off_axis)
            if ((abs(delta_position[0]) == 0 or
                 abs(delta_position[1] == 0))
                    and (off_axis[0] != 0 and off_axis[1] != 0)):
                if abs(off_axis[0]) < abs(off_axis[1]):
                    delta_position[0] += math.copysign(1, off_axis[0])
                else:
                    delta_position[1] += math.copysign(1, off_axis[1])
            self.position = [self.position[0] + delta_position[0],
                             self.position[1] + delta_position[1]]
            print("shark post off axis", delta_position, self.position)

        print("shark going to", self.following_fish, "dist", fish_distance)

        self.previous_moves[0].append(self.position[:2][0])
        self.previous_moves[1].append(self.position[:2][1])
        if len(self.previous_moves[0]) > 8:  # 8 moves have transpired
            self.previous_moves[0].pop(0)
            self.previous_moves[1].pop(0)
        print("shark previous moves", self.previous_moves)
        return self.position


if __name__ == "__main__":
    shark = Shark()
    print(shark.position)
    print(shark.getNextPosition([[1, 1], [1, 2], [1, 3]]))
    print(shark.getNextPosition([[2, 1], [2, 2], [2, 3]]))
