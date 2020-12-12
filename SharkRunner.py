# Sylvia Chin
#
# Shark Runner
#

from Button import Button
from Fish import Fish
from Shark import Shark
from SharkGUI import SharkGUI  

class SharkRunner:

    def __init__(self):
        """Defining variables with self to access other classes
            and initialize fish and shark lists of coordinates"""
        
        # Create the shark graphics window
        self.shark_GUI = SharkGUI()

        # Create 1 shark
        self.shark = Shark()

        # Create an empty list to store fish objects
        self.fishes = []

        #
        self.all_coordinates = [[], [], [], [7,2]]

    def main(self):

        while self.checkFishAlive() and not self.shark.getStalemate():
            action = self.shark_GUI.handleMouse()
            if action == 1:
                # Call start function
                self.start()
            elif action == 2:
                # Call moveFish function
                self.moveFish()
            elif action == 3:
                # Call Shark function
                self.moveShark()

        self.shark_GUI.disableButtons()

        if not self.checkFishAlive():
            self.shark_GUI.displayMessage("Game Over!\n Shark wins.\nClick Quit to exit.")
        else:
            self.shark_GUI.displayMessage("Game Over!\n Fish win.\nClick Quit to exit.")


        # Takes care of quit
        while True:
            self.shark_GUI.handleMouse()

    def checkFishAlive(self):
        if self.fishes:
            return not(self.fishes[0].isDead() and self.fishes[1].isDead()
                       and self.fishes[2].isDead())
        return True

    def start(self):

        fish_coordinates = self.shark_GUI.getCoordinates()

        # Go through each coordinate in the list of coordinates
        for coordinates in fish_coordinates:
            # Check that the length of each fish list is 2
            if len(coordinates) != 2:
                self.shark_GUI.displayMessage("Uh oh! Your coordinates\nshould be 2 numbers.")
                
                return

            # Make sure fish isn't on (7,2) <- shark starting position
            if coordinates == [7,2]:
                self.shark_GUI.displayMessage("Uh oh! One coordinate\nis unavailable")

                return

            # Check coordinates are within the range (0,10)
            if (not(coordinates[0] in range(0,10) and coordinates[1] in
                range(0,10))):
                self.shark_GUI.displayMessage("Uh oh! One coordinate\nis not in range.")

                return

            # Check that coordinates are not the same as other fish
            if fish_coordinates.count(coordinates) >= 2:
                self.shark_GUI.displayMessage("Uh oh! One coordinate is\nalready taken. Acceptable\nrange is [0,9].")

                return

        # Coordinates are locked in
        self.shark_GUI.disableEntry()

        # Set all_coordinates to all fish coordinates
        self.all_coordinates[:3] = fish_coordinates

        # Add all fish coordinates to a list fish
        for i in range(0,3):
            self.fishes.append(Fish(i, fish_coordinates[i]))
            fish_coordinates[i][2] = self.fishes[i].getDirection()
            print("direction of current fish", fish_coordinates[i])

        # Show fish on board
        self.shark_GUI.jumpToCoordinates(fish_coordinates)
        
        # Prompt the player to click the Move button
        self.shark_GUI.displayMessage("Click the Move\nbutton to begin!")

    def moveFish(self):

        # Create empty lists for fleemode and position coordinates
        fleemode = []

        # Go through the fish coordinates list and append fleemode and position
        for i in range(3):
            fleemode.append(self.fishes[i].getFleeMode(self.all_coordinates[3]))
            self.all_coordinates[i] = self.fishes[i].getNextPosition(self.all_coordinates[:])

        print("original flee mode list", fleemode)
        # Connect fleemode fish movements with the graphics
        self.shark_GUI.setFleeMode(fleemode)
        self.shark_GUI.setCoordinates(self.all_coordinates[:3])

        for i in range(3):
            if self.fishes[i].insideWall():
                self.all_coordinates[i] = self.fishes[i].setPosition(
                    self.fishes[i].getThroughWallPosition())
                fleemode[i] = False
                print("agh")

        print("updated flee mode list", fleemode)
        
        # Reset the fleemode list
        self.shark_GUI.setFleeMode(fleemode, 3.5)
                    
    def moveShark(self):

        self.all_coordinates[3] = self.shark.getNextPosition(self.all_coordinates[:3])

        self.shark_GUI.setSharkCoordinates(self.all_coordinates[3])

        dead_fishes = []

        # Check if fish is dead
        for i in range(3):
            if self.all_coordinates[i][:2] == self.all_coordinates[3][:2]:
                if i == 0:
                    self.shark_GUI.displayMessage("Oh no! Orange fish\nhas died. Click the\nMove button to continue.")
                elif i == 1:
                    self.shark_GUI.displayMessage("Oh no! Purple fish\nhas died. Click the\nMove button to continue.")
                elif i == 2:
                    self.shark_GUI.displayMessage("Oh no! Yellow fish\nhas died. Click the\nMove button to continue.")
            if (self.all_coordinates[i][:2] == self.all_coordinates[3][:2]
                or self.fishes[i].isDead()):
                self.fishes[i].setDead(dead_fishes)
                dead_fishes.append(True)
            else:
                dead_fishes.append(False)

        print("Dead fishes:", dead_fishes)

        # Let GUI keep track of dead fishes
        self.shark_GUI.setDead(dead_fishes)
        print("GUI should register fish death")
        

SharkRunner().main()
