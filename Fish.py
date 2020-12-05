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
        """Gets the fishes' next positions based on each others' locations,
            considering flee mode"""

        # Fish moves one spot randomly
            # HAS to move
            # Though doing it this way makes it more likely fish will move
            # along the x-coord than y-coord (only 1/3 chance it moves
            # along the y-coord)
        random_xmove = randrange(-2,2)
        random_ymove = randrange(-2,2)
        randomization = randrange(0,2)
        if randomization == 0:
            self.position[0] += random_xmove
            if random_xmove == 0:
                self.position[1] += random.choice([-1,1])
        elif randomization == 1:
            self.position[1] += random_ymove
            if random_ymove == 0:
                self.position[0] += random.choice([-1,1])

        # Check if fish is next to a wall, make sure it doesn't leave grid
            # Checking left wall, right wall, top wall, bottom wall
        if self.position[0] == 0:
            # If flee mode and planning to go thru wall, enter on other side
            if (self.getFleeMode() and self.position[2] == 180 and
                random_xmove == -1):
                self.position[0] == 10
            # Otherwise turn around and move one
            else:
                self.position[2] == 0
                self.position[0] == 1
        elif self.position[0] == 10:
            if (self.getFleeMode() and self.position[2] == 0 and
                random_xmove == 1):
                self.position[0] == 0
            else:
                self.position[2] == 180
                self.position[0] == 9
        elif self.position[1] == 10:
            if (self.getFleeMode() and self.position[2] == 90 and
                random_ymove == 1):
                self.position[1] == 0
            else:
                self.position[2] == 270
                self.position[0] == 9
        elif self.position[1] == 0:
            if (self.getFleeMode() and self.position[2] == 270 and
                random_ymove == -1):
                self.position[1] == 10
            else:
                self.position[2] == 90
                self.position[0] == 1

        # Make sure no two fish move to the same spot!
        
        # Next fish move is in opposite direction - closest NESW if diagonal
        if self.getFleeMode():
            # Finds angle btwn fish and shark
            shark_direction = math.atan2((self.position[1] - shark_pos[1]),
                                         (self.position[0] - shark_pos[0]))
            # Checks if angle is 0, 90, 180, -90, or -180 (straight)
            if (shark_direction == math.pi or shark_direction == -(math.pi)
                or shark_direction == (math.pi)/2 or shark_direction ==
                -(math.pi)/2 or shark_direction == 0:
                # Set fish's new direction to opposite (-180)
                self.position[2] = (shark_direction) - (math.pi)
                
            # Checks if angle is 45, -45, 135, -135 (diagonal)
                # Fish has to choose randomly btwn the 2 furthest directions
            elif (shark_direction == (math.pi)/4 or shark_direction ==
                  -(math.pi)/4 or shark_direction == (3*math.pi)/4 or
                  shark_direction == -(3*math.pi)/4:
                shark_direction = #not finishing this?
                self.position[2] = randrange #not finishing this?
                  
            # Angle is arbitrary - anything else
            else:
                # Divide by 90, round to nearest int, multiply by 90
                exact_shark_direction = round(math.degrees(shark_direction)//90)
                shark_direction = (exact_shark_direction)*90
                # Closest is directly east from fish
                if shark_direction == 0:
                    # Fish goes west
                    self.position[2] = 180
                # Closest is directly north from fish
                elif shark_direction == 1:
                    # Fish goes south
                    self.position[2] = 270
                # Closest is directly west from fish
                elif shark_direction == 2 or shark_direction == -2:
                    # Fish goes east
                    self.position[2] = 0
                # Closest is directly south from fish
                elif shark_direction = -1:
                    # Fish goes north
                    self.position[2] = 90
                                   
            
        return list

    def getDirection(self) -> int:
        self.direction = init_pos[2]
    
    def getFleeMode(self) -> bool:
        # Checks whether any fish is 3 or less spaces away from shark
            # If so, fleemode is True
        return ((shark_pos[0] - self.position[0]) <= 3 or (shark_pos[1] -
            self.position[1]) <= 3)
            
