#
# Sylvia Chin
#
# Fish class takes care of fish movement, coordinates, "flee" mode,
    # and death
#
from random import randrange

class Fish:

    def __init__(self, fish_id, init_pos: list):
        self.position = init_pos
        self.direction = randrange(0,3)

    def getNextPosition(self, shark_pos: list, otherfishA_pos: list, otherfishB_pos:
                    list) -> list:
        return list

    def getDirection(self) -> int:
        # directions are range(0,3) - n is 0, e is 1, s is 2, w is 3

    def getFleeMode(self) -> bool:
        # Checking whether fish is 3 or less spaces away from shark
        # Next fish move is in opposite direction
    
