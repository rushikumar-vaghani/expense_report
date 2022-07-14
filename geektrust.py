from sys import argv
from const import *
from expense import Expense

def main():

    # Read file name from commadline
    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]

    # Read commands from file
    f = open(file_path, 'r')
    commands = f.readlines()

    # create Expense class object and process command
    expense = Expense()

    # process each command
    for command in commands:
        command_data = command.split()
        if command_data[0] in COMMAND_LIST:
            output = expense.process_command(command_data[0], command_data)
            print(output)
        else:
            print("COMMAND NOT FOUND")

if __name__ == "__main__":
    main()