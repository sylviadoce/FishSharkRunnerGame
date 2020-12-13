# Sylvia Chin
#
# Shark Runner

from Fish import Fish
from Shark import Shark
from SharkGUI import SharkGUI  


class SharkRunner:

    def __init__(self):
        """Initializes variables associated with SharkGUI and Shark
            Class, a list of fish objects, and a list of lists for
            all coordinates"""  
        
        # Creates the shark graphics window
        self.shark_GUI = SharkGUI()

        # Creates 1 shark
        self.shark = Shark()

        # Creates an empty list to store fish objects
        self.fishes = []

        # Creates a list of lists for 3 fish and 1 shark coordinates
        self.all_coordinates = [[], [], [], [7, 2]]

        # List of fish names to identify errors and wins
        self.fish_names = ["orange", "purple", "yellow"]

    def main(self):
        """Runs through each action (certain button clicks) to execute
            the move cycle."""
        
        while self.checkFishAlive() and not self.shark.getStalemate():
            action = self.shark_GUI.handleMouse()
            if action == 1:
                # Call start function
                self.start()
            elif action == 2:
                # Update the move message
                self.shark_GUI.displayMessage("Click the Move\n"
                                              "button to continue!")
                # Call moveFish function
                self.moveFish()
            elif action == 3:
                # Call Shark function
                self.moveShark()

        message = []
        self.shark_GUI.disableButtons()

        # Update the message with the proper winner
        if not self.checkFishAlive():
            self.shark_GUI.displayMessage("Game Over!\nShark wins.\n"
                                          "Click Quit or Try Again.", 2)
        else:
            for i in range(3):
                # Check which specific fish are alive to congratulate
                if not self.fishes[i].isDead():
                    message.append(self.fish_names[i])
            message[0] = message[0].capitalize()
            self.shark_GUI.displayMessage("Shark dies of hunger.\n"
                                          + ", ".join(message) +
                                          " fish(es) win!\n"
                                          "Click Quit or Try Again.", 2)

        while True:
            # Takes care of quit by detecing mouse clicks
            action = self.shark_GUI.handleMouse()
            if action > 0:
                self.shark_GUI.close()
                SharkRunner().main()

    def checkFishAlive(self):
        """Returns True if any fish status is alive"""
        if self.fishes:
            return not(self.fishes[0].isDead() and self.fishes[1].isDead()
                       and self.fishes[2].isDead())
        return True

    def start(self):
        """Sets up round by checking for valid coordinates, displaying
            fishes and shark on board, and deactivating/activating the
            Start and Move buttons"""

        # Gets the inputted fish coordinates from the GUI entry box
        fish_coordinates = self.shark_GUI.getCoordinates()

        # Go through each coordinate in the list of coordinates
        for i in range(2, -1, -1):
            # Check that the length of each fish list is 2
            if len(fish_coordinates[i]) != 2:
                self.shark_GUI.displayMessage(
                    "Uh oh! " + self.fish_names[i].capitalize()
                    + " fish's coord-\ninates should be 2 numbers\n"
                    + "separated by a comma.")
                return

            # Make sure fish isn't on (7,2) <- shark starting position
            if fish_coordinates[i] == [7, 2]:
                self.shark_GUI.displayMessage(
                    "Uh oh! " + self.fish_names[i].capitalize()
                    + " fish's coord-\ninate is on top of shark")
                return

            # Check coordinates are within the range (0,10)
            if (not(fish_coordinates[i][0] in range(0, 10) and
                    fish_coordinates[i][1] in range(0, 10))):
                self.shark_GUI.displayMessage(
                    "Uh oh! " + self.fish_names[i].capitalize()
                    + " fish's coord-\ninate is not in range.\n"
                    "Acceptable range is [0,9].")
                return

            # Check that coordinates are not the same as other fish
            if fish_coordinates.count(fish_coordinates[i]) >= 2:
                self.shark_GUI.displayMessage(
                    "Uh oh! " + self.fish_names[i].capitalize()
                    + " fish's coord-\ninate is already taken.\n"
                    "Acceptable range is [0,9].")
                return

        # Coordinates are locked in
        self.shark_GUI.disableEntry()

        # Set all_coordinates to all fish coordinates
        self.all_coordinates[:3] = fish_coordinates

        # Add all fish coordinates to the fish object list fishes
        for i in range(0, 3):
            self.fishes.append(Fish(i, fish_coordinates[i]))
            fish_coordinates[i][2] = self.fishes[i].getDirection()

        # Show fish on the board
        self.shark_GUI.jumpToCoordinates(fish_coordinates)
        
        # Prompt the player to click the Move button
        self.shark_GUI.displayMessage("Click the Move\nbutton to begin!")

    def moveFish(self):
        """Keeps track of fishes' positions and flee mode status, then
            moves each fish appropriately. Also updates fish recognition
            of going through a wall when in flee mode"""

        # Create a list for fleemode
        fleemode = []

        # Go through the fish coordinates list and append
        # fleemode and position
        for i in range(3):
            fleemode.append(self.fishes[i].getFleeMode(
                self.all_coordinates[3]))
            self.all_coordinates[i] = self.fishes[i].getNextPosition(
                self.all_coordinates[:])

        # Connect fleemode fish movements with the graphics
        self.shark_GUI.setFleeMode(fleemode)
        self.shark_GUI.setCoordinates(self.all_coordinates[:3])

        # Adjust fish coordinates when going through a wall
        for i in range(3):
            if self.fishes[i].insideWall():
                self.all_coordinates[i] = self.fishes[i].setPosition(
                    self.fishes[i].getThroughWallPosition())
                # Deactivate flee mode status once through wall
                fleemode[i] = False
        
        # Reset the fleemode list with a delay of 3.5 seconds
        self.shark_GUI.setFleeMode(fleemode, 3.5)
                    
    def moveShark(self):
        """Keeps track of the shark's positions, then moves it
            appropriately. Also determines whether fish are eaten."""

        # Updates to shark's next position
        self.all_coordinates[3] = self.shark.getNextPosition(
            self.all_coordinates[:3])

        # Updates graphics
        self.shark_GUI.setSharkCoordinates(self.all_coordinates[3])

        dead_fishes = []

        # Check if fish are dead, updates message, stores in
        # dead fishes list
        for i in range(3):
            if self.all_coordinates[i][:2] == self.all_coordinates[3][:2]:
                if i == 0:
                    self.shark_GUI.displayMessage(
                        "Oh no! Orange fish\n has died. Click the\n"
                        "Move button to continue.", 1.5)
                elif i == 1:
                    self.shark_GUI.displayMessage(
                        "Oh no! Purple fish\n has died. Click the\n"
                        "Move button to continue.", 1.5)
                elif i == 2:
                    self.shark_GUI.displayMessage(
                        "Oh no! Yellow fish\nhas died. Click the\n"
                        "Move button to continue.", 1.5)
            if (self.all_coordinates[i][:2] == self.all_coordinates[3][:2]
                    or self.fishes[i].isDead()):
                self.fishes[i].setDead(dead_fishes)
                dead_fishes.append(True)
            else:
                dead_fishes.append(False)

        # Lets GUI keep track of dead fishes
        self.shark_GUI.setDead(dead_fishes)     


# Call main with the SharkRunner class
SharkRunner().main()
