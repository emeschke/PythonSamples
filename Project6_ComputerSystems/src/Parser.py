__author__ = 'E'
#Program takes a line of input and outputs a list of strings representing commandType, symbol, dest, comp, jump in a
#of length 5.



def command_type(line_input, result):
    #Get command type by looking at the first character.
    if line_input[0] == "@":
        result[0] = "A_COMMAND"
    elif line_input[0] == "(":
        result[0]= "L_COMMAND"
    else:
        result[0] = "C_COMMAND"

def symbol(line_input, result):
    #Get the location of an A-Command or and L-Command and store it in location 1
    if line_input[0]=="@":
        result[1] = line_input[1::]
    elif line_input[0]=="(":
        result[1] = line_input[1:-1]
    else:
        result[1] = ""


def dest(line_input, result):
    #For a C-Command, find the dest.
    if result[0] == "C_COMMAND":
        if line_input.find("=") != -1:
            result[2] = line_input.split("=")[0]

def comp(line_input, result):
    #For a C-Command, find the comp.
    if result[0] == "C_COMMAND":
        result[3] = line_input.split(";")[0]
        if result[3].find("=") != -1:
            result[3] = result[3].split("=")[1]

def jump(line_input, result):
    #For a C-Command find the jump.
    if result[0] == "C_COMMAND":
        if line_input.find(";") != -1:
            result[4] = line_input.split(";")[1]

def parser(line_input):
    #Combine all the parts of the line into a list to return.
    output = [""]*5
    command_type(line_input, output)
    symbol(line_input, output)
    dest(line_input, output)
    comp(line_input, output)
    jump(line_input, output)
    return output
