# Sylvia Chin
#
# Shark Runner
#

from Button import Button
from Fish import Fish
from Shark import Shark
from SharkGUI import SharkGUI

def __init__(self):

    # Create the shark graphics window
    shark_GUI = SharkGUI()

    # Create 1 shark
    shark = Shark()

    # Set stalemate position to False
    stalemate = False

    fish = []

def main():

    # Call init to the main function
    __init__()

##    # Create 3 fish
##    fish_A = Fish(fish_A, [])
##    fish_B = Fish(fish_B, [])
##    fish_C =

    while fishAlive and not stalemate:
        action = shark_GUI.handleMouse()
        if action == 1:
            # check flee mode
            adsadsa
        elif action == 2:
            # check flee mode
            ;jads
        elif action == 3:
            ealuhg
            # check if fish is dead
            # check for stalemate

def fishAlive():
    return True

def start():

    # Go through each coordinate in the list of coordinates
    for coordinates in shark_GUI.getCoordinates():
        # Check that the length of each fish list is 2
        if len(coordinates) != 2:
            shark_GUI.displayMessage("Uh oh! Your coordinates should be 2 numbers.")
            
            return

        # Make sure fish isn't on (7,2) <- shark starting position
        if coordinates == [7,2]:
            shark_GUI.displayMessage("Uh oh! This coordinate is unavailable")

            return

        # Check coordinates are within the range (0,10)
        if (coordinates[0] not in range(1,11) or coordinates[1] not in
            range(1,11)):
            shark_GUI.displayMessage("Uh oh! This coordinate is not in range.")

            return

        # Check that coordinates are not the same as other fish
        if shark_GUI.getCoordinates().count(coordinates) > 2:
            shark_GUI.displayMessage("Uh oh! This coordinate is already taken.")
        
        

def moveFish():
    fsdgjkh

def moveShark():
    sdjkflh
