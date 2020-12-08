# Sylvia Chin
#
# Shark Runner
#

from Button import Button
from Fish import Fish
from Shark import Shark
from SharkGUI import SharkGUI  

# Create the shark graphics window
shark_GUI = SharkGUI()

# Create 1 shark
shark = Shark()

fish = []

def main():

    # Set stalemate position to False
    stalemate = False

    while fishAlive and not stalemate:
        action = shark_GUI.handleMouse()
        if action == 1:
            start()
        elif action == 2:
            # check flee mode
            continue
        elif action == 3:
            continue
            # check if fish is dead
            # check for stalemate

def fishAlive():
    return True

def start():

    fish_coordinates = shark_GUI.getCoordinates()

    # Go through each coordinate in the list of coordinates
    for coordinates in fish_coordinates:
        # Check that the length of each fish list is 2
        if len(coordinates) != 2:
            shark_GUI.displayMessage("Uh oh! Your coordinates should be 2 numbers.")
            
            return

        # Make sure fish isn't on (7,2) <- shark starting position
        if coordinates == [7,2]:
            shark_GUI.displayMessage("Uh oh! This coordinate is unavailable")

            return

        # Check coordinates are within the range (0,10)
        if (not(coordinates[0] in range(0,10) and coordinates[1] in
            range(0,10))):
            shark_GUI.displayMessage("Uh oh! This coordinate is not in range.")

            return

        # Check that coordinates are not the same as other fish
        if fish_coordinates.count(coordinates) > 2:
            shark_GUI.displayMessage("Uh oh! This coordinate is already taken. Acceptable range is [0,9].")

            return

    # Coordinates are locked in
    shark_GUI.disableEntry()

    # Add all fish coordinates to a list fish
    for i in range(0,3):
        fish.append(Fish(i, fish_coordinates[i]))
        
    # Show fish on board
    shark_GUI.jumpToCoordinates(fish_coordinates)

def moveFish():
    return

def moveShark():
    return

main()
