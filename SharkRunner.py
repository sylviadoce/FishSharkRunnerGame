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

# Create an empty list to store fish objects
fishes = []

# Set stalemate position to False
stalemate = False

#
all_coordinates = [[], [], [], [7,2]]

def main():

    while fishAlive and not stalemate:
        action = shark_GUI.handleMouse()
        if action == 1:
            # Call start function
            start()
        elif action == 2:
            # Call moveFish function
            moveFish()
        elif action == 3:
            # Call Shark function
            moveShark()

def fishAlive():
    return not(fishes[0].isDead() and fishes[1].isDead() and fishes[2].isDead())

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

    # Set all_coordinates to all fish coordinates
    all_coordinates[:3] = fish_coordinates

    # Add all fish coordinates to a list fish
    for i in range(0,3):
        fishes.append(Fish(i, fish_coordinates[i]))
        
    # Show fish on board
    shark_GUI.jumpToCoordinates(fish_coordinates)
    
    # Prompt the player to click the Move button
    shark_GUI.displayMessage("Click the move button to begin!")

def moveFish():

    # Create empty lists for fleemode and position coordinates
    fleemode = []

    # Go through the fish coordinates list and append fleemod and position
    for i in range(3):
        fleemode.append(fishes[i].getFleeMode(all_coordinates[3]))
        all_coordinates[i] = fishes[i].getNextPosition(all_coordinates[:])

    # Connect fleemode fish movements with the graphics
    shark_GUI.setFleeMode(fleemode)
    shark_GUI.setCoordinates(all_coordinates[:3])

def moveShark():

    all_coordinates[3] = shark.getNextPosition(all_coordinates[:3])

    shark_GUI.setSharkCoordinates(all_coordinates[3])

    dead_fishes = []
    print("Dead fishes:", dead_fishes)

    # Check if fish is dead
    for i in range(3):
        if all_coordinates[i][:2] == all_coordinates[3][:2]:
            print("Shark should be eating fish rn")
            fishes[i].setDead()
            dead_fishes.append(True)
        else:
            dead_fishes.append(False)

    # Let GUI keep track of dead fishes
    shark_GUI.setDead(dead_fishes)
    
    # Check for stalemate
    stalemate = shark.getStalemate()

main()
