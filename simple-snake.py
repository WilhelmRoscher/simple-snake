import os, time, random, sys
from pynput.keyboard import Key, Listener

clear = lambda: os.system('clear')

def print_help():
    print "Simple-Snake (Version 0.1) is a simple snake game written in python.\n"
    print "Usage: python simple-snake.py [-h height] [-w width]\n       [-r refresh-time (speed)] [-f number of fruit] [--help]\n"
    print "Author: Wilhelm Roscher"

    sys.exit(0)

last_key_pressed = ""
score = 0
height = 12
width = 20
refresh_time = 0.2
fruit_number = 1    

# handle arguments (-h -w -r -f --help)
i_argument=0
for argument in sys.argv:
    if argument[0] == "-":
        if argument == "-h":
            try:
                height = int(sys.argv[i_argument + 1])
            except:
                print_help()

        if argument == "-w":
            try:
                width = int(sys.argv[i_argument + 1])
            except:
                print_help()

        if argument == "-r":
            try:
                refresh_time = float(sys.argv[i_argument + 1])
            except:
                print_help()

        if argument == "-f":
            try:
                fruit_number = int(sys.argv[i_argument + 1])
            except:
                print_help()

        if argument == "--help":
            print_help()

    i_argument+=1

# This will store the last key the player pressed. It's used to determine the direction of the snake.
def on_press(key):
    global last_key_pressed
    last_key_pressed = str(key)[2]  # there may be a better way

# This will refresh the playing field on the display.
def refresh(field):
    output = "--" * (width +1) + "- \n" # top part of the frame

    for line in field:
        output += "| " # left part of the frame

        for position in line: output += position

        output += "| \n" # right part of the frame

    output += "--" * (width +1) + "- \n" # bottom part of the frame
    output += "\nScore: " + str(score)

    clear()
    print output

#=== Start of the Game ===

# empty playing field
field = []
for i_line in range(0, height):
    field += [["  "] * width]

# snake on starting position
field[0][0] = "@ "

# initial fruits generation
for i in range(0, fruit_number):
    fruit_position = random.randint(0, width - 1)
    fruit_line = random.randint(0, height - 1)

    # if there allready is something on the field, find a new position
    while field[fruit_line][fruit_position] <> "  ":
        fruit_position = random.randint(0, width - 1)
        fruit_line = random.randint(0, height - 1)

    field[fruit_line][fruit_position] = "* "

refresh(field)

# start keypress listener
with Listener(on_press=on_press) as listener:
    # starting conditions
    head_line = 0
    head_position = 0
    direction = "rightward"
    length = 1
    path = [[0, 0]]
    end = False

    while end <> True:
        # Does the player want to change the direction?
        if (last_key_pressed == "w") and (direction <> "downward"):
            direction = "upward"

        if (last_key_pressed == "a") and (direction <> "rightward"):
            direction = "leftward"

        if (last_key_pressed == "s") and (direction <> "upward"):
            direction = "downward"

        if (last_key_pressed == "d") and (direction <> "leftward"):
            direction = "rightward"

        # replacing the currend snakehead with a snake body-segment
        field[head_line][head_position] = "O "

        # determening the next position of the snake head
        if direction == "upward":
            head_line-=1
            if head_line < 0: head_line = height-1

        if direction == "leftward":
            head_position-=1
            if head_position < 0: head_position = width-1

        if direction == "downward":
            head_line+=1
            if head_line == height: head_line = 0

        if direction == "rightward":
            head_position+=1
            if head_position == width: head_position = 0

        path += [[head_line, head_position]]
        # Has the snake bitten itself?
        if field[head_line][head_position] == "O ":
            end = True

        # Fruit found?
        if field[head_line][head_position] == "* ":
            score += 15
            length += 1

            # place a new fruit

            fruit_position = random.randint(0, width - 1)
            fruit_line = random.randint(0, height - 1)

            # if there allready is something on the field, find a new position
            while field[fruit_line][fruit_position] <> "  ":
                fruit_position = random.randint(0, width - 1)
                fruit_line = random.randint(0, height - 1)

            field[fruit_line][fruit_position] = "* "

        # remove the last snake-segment from the field
        [last_segment_line, last_segment_position] = path[len(path)-length - 1]
        field[last_segment_line][last_segment_position] = "  "

        # place the sneaks head
        field[head_line][head_position] = "@ "
        refresh(field)
        time.sleep(refresh_time)
    
# display ending text
output = "--" * (width +1) + "- \n" # top part of the frame
for line in field:
    output += "| " # left part of the frame
    for position in line: output += position
    output += "| \n" # right part of the frame
output += "--" * (width +1) + "- \n" # bottom part of the frame
clear()
print output

print "Game Over.\n"
print "Score " + str(score)
print "\nlook at --help for more options"
