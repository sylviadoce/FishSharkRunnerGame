# Sylvia Chin
#
# Fish class takes care of fish movement, coordinates, "flee" mode,
# and death

import random
import math


class Fish:

    def __init__(self, fish_id, init_pos: list):
        """Initializes the fish's position (a list of x-coord, y-coord,
            its id, its state of death (False) and a randomized
            direction NESW)."""

        self.position = init_pos
        self.fish_id = fish_id
        self.dead = False
        self.position.append((random.randrange(0, 3))*90)

    def getNextPosition(self, all_coordinates: list) -> list:
        """Gets the fishes' next positions based on if it's alive,
            if it's in flee mode, if it's facing a wall, and if it's on
            another's location."""

        # Pop fish_id from the all_coordinates list
        all_coordinates.pop(self.fish_id)

        # Check if fish is dead and move off the grid
        if self.dead:
            return [-10, -10]
        # Check for flee mode relative to shark's position
        if self.getFleeMode(all_coordinates[2]):
            # Special get next position method
            return self.getFleeModeNextPosition(all_coordinates)
##        # Prevents fish from swapping places (overlapping)
##        if self.facingEachOther(self.getXY(), all_coordinates):
##            return self.position
        # Turn the fish around if facing a wall
        if self.facingWall():
            self.position[2] += 180
            self.position[2] %= 360
        # Compare the all fishes' and shark's next positions
        if self.sameNextPosition(self.getXY(), all_coordinates):
            return self.position

        # New position is the calculated next position
        self.position[:2] = self.getXY() 
        
        return self.position[:2]

    def getXY(self) -> list:
        """Gets fish's next move along the x or y-axis."""

        # Use trig on the fish's direction to determine movement
        # Because of python coordinate system, subtract y movement
        return [self.position[0] +
                round(math.cos(math.radians(self.position[2]))),
                self.position[1] -
                round(math.sin(math.radians(self.position[2])))]

    def getDirection(self) -> int:
        """Gets the direction z from the list x, y, z of fish."""

        return self.position[2]

    def facingWall(self) -> bool:
        """Determines if fish is about to go into wall - on it and
            facing it."""

        if ((self.position[0] <= 0 and self.position[2] == 180) or
                (self.position[0] >= 9 and self.position[2] == 0) or
                (self.position[1] <= 0 and self.position[2] == 90) or
                (self.position[1] >= 9 and self.position[2] == 270)):
            return True
        else:
            return False
        
    def insideWall(self) -> bool:
        """Determines if fish is inside the wall."""

        return (self.position[0] <= -1 or self.position[0] >= 10 or
                self.position[1] <= -1 or self.position[1] >= 10)

    def sameNextPosition(self, position: list,
                         all_coordinates: list) -> bool:
        """Returns True if two fish are moving to the same position,
            starting with the first fish."""

##        print("og POSITION LIST:", position)
##        print("og ALL COORDS LIST:", all_coordinates)
##        print("og SELF.POS LIST:", self.position)
##
##        og_positions = [[self.position[:2]], [all_coordinates[0][:2]],
##                        [all_coordinates[1][:2]]]
##
##        print("init og poses:", og_positions)

        if self.fish_id == 0:
            return False
        elif self.fish_id == 1:
            return (position[:2] == all_coordinates[0][:2])
        elif self.fish_id == 2:
            return (position[:2] == all_coordinates[1][:2] or
                    position[:2] == all_coordinates[0][:2])

##    def facingEachOther(self, position: list,
##                        all_coordinates: list) -> bool:
##        """Returns True if two fishes are about to swap positions."""
##
##        if self.fish_id == 0:
##            return (self.position[:2] == all_coordinates[0][:2] and
##                    position[:2] == #og position of other fish
##                    or self.position[:2] == all_coordinates[1][:2] and
##                    position[:2] == #og position of other fish
##        elif self.fish_id == 1:
##            return (self.position[:2] == all_coordinates[0][:2] and
##                    position[:2] == #og position of other fish
##                    or self.position[:2] == all_coordinates[1][:2] and
##                    position[:2] == #og position of other fish
##        elif self.fish_id == 2:
##            return (position[:2] == self.position[:2] or
##                    position[:2] == self.position[:2])

    def getThroughWallPosition(self) -> list:
        """Detecting in flee mode that fish goes through the wall,
            returns new position.""" 

        if self.position[0] <= 0 and self.position[2] == 180:
            return [9, self.position[1]]
        elif self.position[0] >= 9 and self.position[2] == 0:
            return [0, self.position[1]]
        elif self.position[1] <= 0 and self.position[2] == 90:
            return [self.position[0], 9]
        elif self.position[1] >= 9 and self.position[2] == 270:
            return [self.position[0], 0]

    def setPosition(self, position: list) -> list:
        """Sets the new position to self.position."""
        
        self.position[:2] = position[:2]
        
        return self.position[:2]

    def getFleeMode(self, shark_pos: list) -> bool:
        """Returns True if the shark is 3 or less spaces away
            from a fish."""

        return ((abs(shark_pos[0] - self.position[0]) <= 3) and
                (abs(shark_pos[1] - self.position[1]) <= 3))

    def getFleeModeNextPosition(self, all_coordinates: list) -> list:
        """Determines fish's next position based on shark's angle in
            flee mode."""

        # Finds directional angle between fish/shark, convert to
        # degrees, [0,360) interval
        shark_direction = math.degrees(
            -math.atan2((self.position[1] - all_coordinates[2][1]),
                        (self.position[0] - all_coordinates[2][0]))) % 360
        
        # Checks if angle is 0, 90, 180, 270 (straight)
        if shark_direction % 90 == 0:
            # Set fish's new direction to opposite
            self.position[2] = shark_direction % 360
            
        # Checks if angle is 45, 135, 225, 315 (diagonal)
        # Fish has to choose randomly between the 2 farthest directions
        elif (shark_direction - 45) % 90 == 0:
            self.position[2] = shark_direction
            choice = random.choice([-45, 45])
            self.position[2] += choice
            self.position[2] %= 360

            # If the chosen direction's position is taken, choose the other
            if self.sameNextPosition(self.getXY(), all_coordinates):
                if choice == -45:
                    self.position[2] += 90
                else:
                    self.position[2] += -90
              
        # Angle is arbitrary - anything else
        else:
            # Divide by 90, round to nearest int, multiply by 90
            self.position[2] = (round(shark_direction/90) * 90) % 360

        # Check if next position is facing wall, if so go through wall
        check_position = self.getXY()
        if self.facingWall():
            check_position = self.getThroughWallPosition()

        # Check if next position (other option) is taken, if so don't move
        if self.sameNextPosition(check_position, all_coordinates):
            return self.position
        else:
            self.position[:2] = self.getXY()
            return self.position[:2]

    def setDead(self, dead):
        """Sets fish status to dead."""
        
        self.dead = dead

    def getPosition(self):
        """Get the next position: x, y, z."""
        
        return self.position

    def isDead(self):
        """Checks if fish status is dead."""
        
        return self.dead
