# Sylvia Chin
#
# Fish class takes care of fish movement, coordinates, "flee" mode,
    # and death
#
from random import randrange
import math

class Fish:

    def __init__(self, fish_id, init_pos: list):
        """Sets the fish position to a list of x-coord, y-coord, and
            a randomized direction NESW"""
        
        self.position = init_pos
        self.direction = (randrange(0,3))*90

    def getNextPosition(self, shark_pos: list, otherfishA_pos: list,
                        otherfishB_pos: list) -> list:
        
       fleemode = self.getFleeMode()
        
        # Next fish move is in opposite direction
        if fleemode:
            math.atan2((self.position[1]-shark_pos[1]), (self.position[0] -
                                                      shark_pos[0]))
            
        return list

    def getDirection(self) -> int:
        # directions are range(0,3) - n is 0, e is 1, s is 2, w is 3
    
    def getFleeMode(self) -> bool:
        # Checks whether any fish is 3 or less spaces away from shark
            # If so, fleemode is True
        return ((shark_pos[0] - self.position[0]) <= 3 or (shark_pos[1] -
            self.position[1]) <= 3)
            
