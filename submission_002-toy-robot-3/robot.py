import sys
from io import StringIO
import re
# list of valid command names
valid_commands = ['off', 'help', 'forward', 'back', 'right', 'left', 'sprint','history','replay']

# variables tracking position and direction
position_x = 0
position_y = 0
directions = ['forward', 'right', 'back', 'left']
current_direction_index = 0

# area limit vars
min_y, max_y = -200, 200
min_x, max_x = -100, 100

#initilize history to an empty list to append commands to history
history = []


#TODO: WE NEED TO DECIDE IF WE WANT TO PRE_POPULATE A SOLUTION HERE, OR GET STUDENT TO BUILD ON THEIR PREVIOUS SOLUTION.

def get_robot_name():
    name = input("What do you want to name your robot? ")
    while len(name) == 0:
        name = input("What do you want to name your robot? ")
    return name


def get_command(robot_name):
    """
    Asks the user for a command, and validate it as well
    Only return a valid command
    """

    prompt = ''+robot_name+': What must I do next? '
    command = input(prompt)
    while len(command) == 0 or not valid_command(command.lower()):
        output(robot_name, "Sorry, I did not understand '"+command+"'.")
        command = input(prompt)
    
    add_commands_history(command.lower())

    return command.lower()


def split_command_input(command):
    """
    Splits the string at the first space character, to get the actual command, as well as the argument(s) for the command
    :return: (command, argument)
    """
    args = command.split(' ', 1)
    if len(args) > 1:
        return args[0], args[1]
    return args[0], ''


def is_int(value):
    """
    Tests if the string value is an int or not
    :param value: a string value to test
    :return: True if it is an int
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


def valid_command(command):
    """
    Returns a boolean indicating if the robot can understand the command or not
    Also checks if there is an argument to the command, and if it a valid int
    """

    (command_name, arg1) = split_command_input(command)
    if len(arg1.split(' ')) < 2:
        return command_name.lower() in valid_commands and (len(arg1) == 0 or is_int(arg1) or re.search("\d-\d",arg1) or arg1 == 'silent' or arg1 == 'reversed')
    else:
        (arg1,arg2) = split_command_input(arg1)
        return command_name.lower() in valid_commands and ((arg1 == 'reversed' and arg2 == 'silent') or ((is_int(arg1) or re.search("\d-\d",arg1)) and (arg2 == 'silent' or arg2 == 'reversed')))


def output(name, message):
    print(''+name+": "+message)


def do_help():
    """
    Provides help information to the user
    :return: (True, help text) to indicate robot can continue after this command was handled
    """
    return True, """I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD - move forward by specified number of steps, e.g. 'FORWARD 10'
BACK - move backward by specified number of steps, e.g. 'BACK 10'
RIGHT - turn right by 90 degrees
LEFT - turn left by 90 degrees
SPRINT - sprint forward according to a formula
HISTORY - keeps a history of the commands given to it
REPLAY -  filter out all non-movement commands and redo only the movement commands
"""


def show_position(robot_name):
    print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')


def is_position_allowed(new_x, new_y):
    """
    Checks if the new position will still fall within the max area limit
    :param new_x: the new/proposed x position
    :param new_y: the new/proposed y position
    :return: True if allowed, i.e. it falls in the allowed area, else False
    """

    return min_x <= new_x <= max_x and min_y <= new_y <= max_y


def update_position(steps):
    """
    Update the current x and y positions given the current direction, and specific nr of steps
    :param steps:
    :return: True if the position was updated, else False
    """

    global position_x, position_y
    new_x = position_x
    new_y = position_y

    if directions[current_direction_index] == 'forward':
        new_y = new_y + steps
    elif directions[current_direction_index] == 'right':
        new_x = new_x + steps
    elif directions[current_direction_index] == 'back':
        new_y = new_y - steps
    elif directions[current_direction_index] == 'left':
        new_x = new_x - steps

    if is_position_allowed(new_x, new_y):
        position_x = new_x
        position_y = new_y
        return True
    return False


def do_forward(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    if update_position(steps):
        return True, ' > '+robot_name+' moved forward by '+str(steps)+' steps.'
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'


def do_back(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """

    if update_position(-steps):
        return True, ' > '+robot_name+' moved back by '+str(steps)+' steps.'
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'


def do_right_turn(robot_name):
    """
    Do a 90 degree turn to the right
    :param robot_name:
    :return: (True, right turn output text)
    """
    global current_direction_index

    current_direction_index += 1
    if current_direction_index > 3:
        current_direction_index = 0

    return True, ' > '+robot_name+' turned right.'


def do_left_turn(robot_name):
    """
    Do a 90 degree turn to the left
    :param robot_name:
    :return: (True, left turn output text)
    """
    global current_direction_index

    current_direction_index -= 1
    if current_direction_index < 0:
        current_direction_index = 3

    return True, ' > '+robot_name+' turned left.'


def do_sprint(robot_name, steps):
    """
    Sprints the robot, i.e. let it go forward steps + (steps-1) + (steps-2) + .. + 1 number of steps, in iterations
    :param robot_name:
    :param steps:
    :return: (True, forward output)
    """

    if steps == 1:
        return do_forward(robot_name, 1)
    else:
        (do_next, command_output) = do_forward(robot_name, steps)
        print(command_output)
        return do_sprint(robot_name, steps - 1)


def handle_command(robot_name, command):
    """
    Handles a command by asking different functions to handle each command.
    :param robot_name: the name given to robot
    :param command: the command entered by user
    :return: `True` if the robot must continue after the command, or else `False` if robot must shutdown
    """

    (command_name, arg) = split_command_input(command)

    if command_name == 'off':
        return False
    elif command_name == 'help':
        (do_next, command_output) = do_help()
    elif command_name == 'forward':
        (do_next, command_output) = do_forward(robot_name, int(arg))
    elif command_name == 'back':
        (do_next, command_output) = do_back(robot_name, int(arg))
    elif command_name == 'right':
        (do_next, command_output) = do_right_turn(robot_name)
    elif command_name == 'left':
        (do_next, command_output) = do_left_turn(robot_name)
    elif command_name == 'sprint':
        (do_next, command_output) = do_sprint(robot_name, int(arg))
    elif(command_name == 'history'):
        (do_next,command_output) = add_commands_history(command,int(arg))
    elif('replay' in command_name ):
        (do_next,command_output) = replay(robot_name,command)

    print(command_output)
    show_position(robot_name)
    return do_next

def add_commands_history(command):
    global history
    history.append(command)
    return history

def replay(robot_name,command):
    global history
    
    index = len(history)
    history.pop(index-1)
    
    (command_name,arg1) = split_command_input(command)
    filtered_list = ['off','help','history','replay','replay silent','replay reversed silent']
    filtered_commands = list(filter(lambda command: command not in filtered_list, history))
    
    n = len(filtered_commands)
    m = 0
    (arg1,arg2) = split_command_input(arg1)
    if is_int(arg1):
        n = int(arg1)
    elif re.search("\d-\d",arg1):
        n = int(arg1[0])
        m = int(arg1[2])
    # print(filtered_commands)
    if 'reversed' in command:
        filtered_commands = filtered_commands[::-1]
        # print(filtered_commands)
    filtered_commands = [filtered_commands[i] for i in range(len(filtered_commands)-n,len(filtered_commands)-m)]
    # print(filtered_commands)
        

    number_of_commands = len(filtered_commands)
    if 'reversed silent' in command.lower():
        new_output = StringIO()
        old_output = sys.stdout
        sys.stdout = new_output
        for command in filtered_commands:
            handle_command(robot_name, command)
        sys.stdout = old_output
        return True,' > '+robot_name+' replayed '+str(number_of_commands)+' commands in reverse silently.'
    elif 'silent' in command.lower():
        new_output = StringIO()
        old_output = sys.stdout
        sys.stdout = new_output
        for command in filtered_commands:
            handle_command(robot_name, command)
        sys.stdout = old_output
        return True,' > '+robot_name+' replayed '+str(number_of_commands)+' commands silently.'
    elif 'reversed' in command.lower():
        for commands in filtered_commands:
            handle_command(robot_name, commands)
    
        return True,' > '+robot_name+' replayed '+str(number_of_commands)+' commands in reverse.'
    
    else:
        for commands in filtered_commands:
            handle_command(robot_name, commands)
    
        return True,' > '+robot_name+' replayed '+str(number_of_commands)+' commands.'

def robot_start():
    """This is the entry point for starting my robot"""

    global position_x, position_y, current_direction_index, history

    robot_name = get_robot_name()
    output(robot_name, "Hello kiddo!")

    position_x = 0
    position_y = 0
    current_direction_index = 0
    history = []

    command = get_command(robot_name)
    while handle_command(robot_name, command):
        command = get_command(robot_name)

    output(robot_name, "Shutting down..")


if __name__ == "__main__":
    robot_start()
