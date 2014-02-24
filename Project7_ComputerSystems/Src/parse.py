__author__ = 'E'

#Function takes a filename.  Returns a list of parsed lines or a blank list if file is not read, there is no information
#or the file suffix is not vm.
poss_commands = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not", "push", "pop"]


def read_file(filename):
#Get the content out of the file line by line, return it in a list.
    try:
        with open(filename) as inputFile:
            content = inputFile.readlines()
            return content
    except IOError:
        print "Input file not found.  Please check the path and filename and try again."
        return []


def line_parser(line):
    #Split the line.  Worry about comments and blank lines later.
    split_line=line.split(" ")
    #Return a 3 item list, blanks for items that don't exist.  Otherwise return a blank list.
    if len(split_line) == 1:
        return [split_line[0].strip(), "", ""]
    elif len(split_line) == 2:
        return [split_line[0].strip(), split_line[1].strip(), ""]
    elif len(split_line) == 3:
        return [split_line[0].strip(), split_line[1].strip(), split_line[2].strip()]
    else:
        return ["", "", ""]

def parser_file(filename):
    #Get the content from the file.
    content = read_file(filename)
    parsed_list = []
    #Parse each line of the content and append it into the parsed list using line_parser function.
    for i in content:
        #Parse line and add it to the parsed_list for the file if it's first command is valid.
        #This removes the comment lines and blank lines from the list.
        parsed_line = line_parser(i)
        if parsed_line[0] in poss_commands:
            parsed_list.append(parsed_line)
    return parsed_list



