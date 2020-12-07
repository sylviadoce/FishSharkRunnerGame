# Sylvia Chin
#
# Fish class takes care of fish movement, coordinates, "flee" mode,
    # and death
#
import random
import math

class Fish:

    def __init__(self, fish_id, init_pos: list):
        """Sets the fish position to a list of x-coord, y-coord, and
            a randomized direction NESW"""
        
        self.position = init_pos
        self.fish_id = fish_id
        self.dead = False
        self.position.append((random.randrange(0,3))*90)

    def getNextPosition(self, shark_pos: list, otherfishA_pos: list,
                        otherfishB_pos: list) -> list:
        """Gets the fishes' next positions based on each others' locations,
            considering flee mode"""

        # Check if fish is dead and move off the grid
        if self.dead:
            return [-10,-10]
        if self.getFleeMode():
            return self.getFleeModeNextPosition()
            # include if facing wall and if in same fish
        if self.facingWall():
            self.position[2] += 180
            self.position[2] %= 360
        if self.sameNextPosition():
            return self.position

        self.position[0] = math.cos(self.position[2])
        self.position[1] = math.sin(self.position[2])
        return self.position            
            
        # Save original position
        og_pos = self.position

        # Fish continues in its random direction
        dgjklhs
        
##        random_xmove = random.randrange(-1,2)
##        random_ymove = random.randrange(-1,2)
##        randomization = random.randrange(0,2)
##        if randomization == 0:
##            self.position[0] += random_xmove
##            if random_xmove == 0:
##                self.position[1] += random.choice([-1,1])
##        elif randomization == 1:
##            self.position[1] += random_ymove
##            if random_ymove == 0:
##                self.position[0] += random.choice([-1,1])

        # Check if fish is next to a wall, make sure it doesn't leave grid
            # Checking left wall, right wall, top wall, bottom wall
        if self.position[0] == 0:
            # If flee mode and planning to go thru wall, enter on other side
            if (self.getFleeMode() and self.position[2] == 180 and
                random_xmove == -1):
                self.position[0] = 10
            # Otherwise turn around and move one
            else:
                self.position[2] = 0
                self.position[0] = 1
        elif self.position[0] == 10:
            if (self.getFleeMode() and self.position[2] == 0 and
                random_xmove == 1):
                self.position[0] = 0
            else:
                self.position[2] = 180
                self.position[0] = 9
        elif self.position[1] == 10:
            if (self.getFleeMode() and self.position[2] == 90 and
                random_ymove == 1):
                self.position[1] = 0
            else:
                self.position[2] = 270
                self.position[0] = 9
        elif self.position[1] == 0:
            if (self.getFleeMode() and self.position[2] == 270 and
                random_ymove == -1):
                self.position[1] = 10
            else:
                self.position[2] = 90
                self.position[0] = 1
        
        # Next fish move is in opposite direction - closest NESW if diagonal
        if self.getFleeMode():
            
            
        return list

    def getDirection(self) -> int:
        "Gets the direction z from the list x, y, z of self"
        
        self.direction = init_pos[2]

    def facingWall(self) -> bool:
        "Determines if fish is about to go into wall"
        
        return ((self.position[0] == 0 and self.position[2] == 180) or
                (self.position[0] == 9 and self.position[2] == 0) or
                (self.position[1] == 0 and self.position[2] == 90) or
                (self.position[1] == 9 and self.position[2] == 270))

    def sameNextPosition(self) -> bool:
        "Returns True if two fish are moving to the same position"
        return (self.position[:2] == otherfishA_pos[:2] or self.position[:2] ==
            otherfishB_pos[:2])
    
    def getFleeMode(self) -> bool:
        "Returns True if the shark is 3 or less spaces away from a fish"

        return ((shark_pos[0] - self.position[0]) <= 3 or (shark_pos[1] -
            self.position[1]) <= 3)

    def getFleeModeNextPosition(self, shark_pos: list, otherfishA_pos: list,
                        otherfishB_pos: list) -> list:
        "Determines fish's next position based on shark's angle in flee mode"
        
        # Finds angle btwn fish/shark, convert to degrees, [0,360) interval
        shark_direction = math.degrees(
            math.atan2((self.position[1] - shark_pos[1]),
                       (self.position[0] - shark_pos[0]))) % 360
        
        # Checks if angle is 0, 90, 180, 270 (straight)
        if shark_direction % 90 == 0:
            # Set fish's new direction to opposite
            self.position[2] = (shark_direction + 180) % 360
            
        # Checks if angle is 45, 135, 225, 315(diagonal)
            # Fish has to choose randomly btwn the 2 farthest directions
        elif (shark_direction - 45) % 90 == 0:
            self.position[2] += random.choice([-45, 45])
            self.position[2] %= 360
              
        # Angle is arbitrary - anything else
        else:
            # Divide by 90, round to nearest int, multiply by 90
            self.position[2] = ((round((shark_direction)/90)) * 90) % 360

        # Check if facing wall
        if self.facingWall():
            

        # Check if on another fish
        if self.sameNextPosition():

            
