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

    def getNextPosition(self, all_coordinates: list) -> list:
        """Gets the fishes' next positions based on each others' locations,
            considering flee mode"""

        print("getting next position")

        # Pop fish_id from the all_coordinates list
        all_coordinates.pop(self.fish_id)

        # Check if fish is dead and move off the grid
        if self.dead:
            return [-10,-10]
        if self.getFleeMode(all_coordinates[2]):
            return self.getFleeModeNextPosition(all_coordinates)
        if self.facingWall():
            print("yes, facing wall and running code")
            self.position[2] += 180
            self.position[2] %= 360
        if self.sameNextPosition(self.getXY(), all_coordinates):
            print("yes same next pos")
            return self.position

        # self.position[:2] = self.getXY() doesn't work - issue is associated
        # with self.getXY() as a parameter because it doubles
        
        return self.getXY() 

    def getXY(self) -> list:
        "Gets next move along x or y axis"

        print("list of self.position:", self.position)

        print("OG fish direction:", self.position[2])

        print("OG positions:", self.position[0], self.position[1])
        print("OG direction:", self.position[2])

        print("rounded adding to x:", round(math.cos(math.radians(self.position[2]))))
        print("rounded adding to y:", -round(math.sin(math.radians(self.position[2]))))
        
        return [self.position[0] + round(math.cos(math.radians(self.position[2]))),
                self.position[1] - round(math.sin(math.radians(self.position[2])))]


    def getDirection(self) -> int:
        "Gets the direction z from the list x, y, z of self"

        return self.position[2]

    def facingWall(self) -> bool:
        "Determines if fish is about to go into wall"

        if ((self.position[0] == 0 and self.position[2] == 180) or
                (self.position[0] == 9 and self.position[2] == 0) or
                (self.position[1] == 0 and self.position[2] == 90) or
                (self.position[1] == 9 and self.position[2] == 270)):
            print("facing a wall")
            return True
        else:
            print("not facing a wall")
            return False
        
##        return ((self.position[0] == 0 and self.position[2] == 180) or
##                (self.position[0] == 9 and self.position[2] == 0) or
##                (self.position[1] == 0 and self.position[2] == 90) or
##                (self.position[1] == 9 and self.position[2] == 270))

    def sameNextPosition(self, position: list, all_coordinates: list) -> bool:
        "Returns True if two fish are moving to the same position"

        print("position list in samenextposition:", position)
        print("all coordinates in same next pos:", all_coordinates)
        
        return (position[:2] == all_coordinates[0][:2] or position[:2] ==
            all_coordinates[1][:2])

    def getThroughWallPosition(self) -> list:
        """Detecting in flee mode that fish goes through the wall,
            returns new position""" 

        if self.position[0] == 0:
            return [9, self.position[1]]
        elif self.position[0] == 9:
            return [0, self.position[1]]
        elif self.position[1] == 0:
            return [self.position[0], 9]
        elif self.position[1] == 9:
            return [self.position[0], 0]

    def getFleeMode(self, shark_pos: list) -> bool:
        "Returns True if the shark is 3 or less spaces away from a fish"

        print("shark init pos:", shark_pos)
        print("fish position:", self.position)
        
        return (abs((shark_pos[0] - self.position[0]) <= 3) and
                abs((shark_pos[1] - self.position[1])) <= 3)

    def getFleeModeNextPosition(self, all_coordinates: list) -> list:
        "Determines fish's next position based on shark's angle in flee mode"

        print("moving flee mode")
        
        # Finds angle btwn fish/shark, convert to degrees, [0,360) interval
        shark_direction = math.degrees(
            math.atan2(math.radians(self.position[1] - all_coordinates[2][1]),
                       math.radians(self.position[0] - all_coordinates[2][0]))) % 360

        print("shark direction relative to fish:", shark_direction)
        
        # Checks if angle is 0, 90, 180, 270 (straight)
        if shark_direction % 90 == 0:
            print("shark is on axis")
            # Set fish's new direction to opposite
            self.position[2] = (shark_direction + 180) % 360
            print("altered fish direction oppo:", self.position[2])
            
        # Checks if angle is 45, 135, 225, 315(diagonal)
            # Fish has to choose randomly btwn the 2 farthest directions
        elif (shark_direction - 45) % 90 == 0:
            print("shark on 45")
            self.position[2] = (shark_direction + 180)
            print("altered fish direction oppo:", self.position[2])
            choice = random.choice([-45, 45])
            self.position[2] += choice
            self.position[2] %= 360
            print("randomized direction choice:", self.position[2])

            if self.sameNextPosition(self.getXY(), all_coordinates):
                if choice == -45:
                    self.position[2] += 90
                else:
                    self.position[2] += -90
              
        # Angle is arbitrary - anything else
        else:
            print("shark angled, og fish direction:", self.position[2])
            # Divide by 90, round to nearest int, multiply by 90
            self.position[2] = ((round(shark_direction/90) * 90) + 180) % 360
            print("altered fish direction oppo:", self.position[2])

        # Check if facing wall, exclude direction, of next position
        check_position = self.getXY()
        if self.facingWall():
            check_position = self.getThroughWallPosition()

        # Check if on another fish
        if self.sameNextPosition(check_position, all_coordinates):
            return self.position
        else:
            # fish has another option
            return self.getXY()

    def setDead(self, dead):
        "Defining death"
        
        self.dead = dead

    def getPosition(self):
        return self.position

    def isDead(self):
        return self.dead
