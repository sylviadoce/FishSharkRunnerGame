# Benjamin Antupit

# Shark class: Gets shark position and keeps track of stalemates

import math
from random import sample


class Shark:

    def __init__(self):
        """Create new shark at [7,2]"""
        self.position = [7, 2, 0]
        self.max_distance = 2.49  # Max direct distance
        self.following_fish = -1
        self.previous_moves = [[], []]

    def getStalemate(self):
        """Return whether shark will be forever hungry"""
        # Return False for the first 12 moves.
        # No stalemate can occur before then
        if len(self.previous_moves[0]) >= 12:  # 12 moves have transpired
            # Count x and y coordinates which are the same as
            # the first in the list
            return (self.previous_moves[0].count(
                self.previous_moves[0][0]) == len(self.previous_moves[0])
                    or self.previous_moves[1].count(
                self.previous_moves[1][0]) == len(self.previous_moves[1]))
        return False

    def getPosition(self):
        """Returns current position in [x,y]"""
        return self.position[:2]

    def getNextPosition(self, fish_pos: list) -> list:
        """Calculate and return next shark position"""
        distances = []
        # Create list of distances to each fish
        for pos in fish_pos:
            distances.append(math.dist(pos[:2], self.position[:2]))
        # Check if 2 or 3 fish have equal distances
        if ((sorted(distances)[0] == sorted(distances)[1] and
             0 <= sorted(distances).index(
                    distances[self.following_fish]) <= 1) or
            (sorted(distances)[0] == sorted(distances)[1]
                == sorted(distances)[2])
                and self.following_fish > 0):
            closest_fish = fish_pos[self.following_fish]
        else:
            # Choose one of the equally-distanced fish at random
            self.following_fish = distances.index(
                min(sample(distances, 3)))
            closest_fish = fish_pos[self.following_fish]
        fish_distance = math.dist(closest_fish[:2], self.position[:2])
        if fish_distance > 0.4:  # Check if shark is not on fish
            delta_position = [
                round(min(self.max_distance, fish_distance) * (
                    (closest_fish[0] - self.position[0]) / fish_distance)),
                round(min(self.max_distance, fish_distance) * (
                    (closest_fish[1] - self.position[1]) / fish_distance))]
            off_axis = [closest_fish[0] - self.position[0],
                        closest_fish[1] - self.position[1]]
            # Prefer moving diagonally if shark if not on-axis with a fish
            if ((abs(delta_position[0]) == 0 or
                 abs(delta_position[1] == 0))
                    and (off_axis[0] != 0 and off_axis[1] != 0)):
                if abs(off_axis[0]) < abs(off_axis[1]):
                    delta_position[0] += math.copysign(1, off_axis[0])
                else:
                    delta_position[1] += math.copysign(1, off_axis[1])
            self.position = [self.position[0] + delta_position[0],
                             self.position[1] + delta_position[1]]
        # save current move to previous_moves for stalemate detection
        self.previous_moves[0].append(self.position[:2][0])
        self.previous_moves[1].append(self.position[:2][1])
        # Clean previous_moves list if longer than 12
        if len(self.previous_moves[0]) > 12:  # 12 moves have transpired
            self.previous_moves[0].pop(0)
            self.previous_moves[1].pop(0)
        return self.position
