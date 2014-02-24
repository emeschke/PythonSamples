__author__ = 'Eric Meschke'

import sys
from Strip_line import *

#Get the name of the file including the file path or return None if the file doesn't end with ".in".
def get_file_name(input):
    #Check that the end of the file ends with .in, if not return None
    if input[-3::] != '.in':
        return None
    #Return the string minus the .in at the end of the file name.
    else:
        return input[0:-3]


def main():
    #Get the output name of the file.  This function returns None if the filename doesn't end in .in and the program
    #exits if no argv for the filename is entered.
    output = ""
    new_output = ""
    if len(sys.argv) <2:
        print "Please enter appropriate command line arguments."
        return 1
    else:
        output = get_file_name(sys.argv[1])

    #Check if the output is none.  If it is, exit, otherwise set the file output name.
    if output is None:
        print "Input file is not valid, does not end with .in extension.  No output written."
        return 1
    else:
        output += ".out"

    #Try to open the input file and read in the contents.  If it won't open print error and exit.  Using with/open has
    #the advantage of closing the file after the suite finishes.
    try:
        with open(str(sys.argv[1])) as inputFile:
            content = inputFile.readlines()
    except IOError:
        print "Input file not found.  Please check the path and filename and try again."
        return 1

    #Try to open the output file.  Because it will create/overwrite there should be no problem with opening it, but
    #still good practice to handle the exception.

    try:
        with open(output, "w") as outputFile:
            print "Files opened successfully."
            for i in content:
                #Check if the no-comments is requested, if so, call the function that removes the comments.
                if len(sys.argv)>=3 and sys.argv[2] == "no-comments":
                    i = remove_comments(i)
                #Remove the space from the line using the strip line function.
                i = strip_line(i)
                #If the entire line is a new line then it is a blank line, don't print to file.  Also check for the
                # carriage return in linux which is \r rather than \n
                if i == '\n' or i == '\r' or i == '\r\n' or len(i) == 0:
                    pass
                else:
                    outputFile.writelines(i)
    except IOError:
        #If it couldn't print to output, exit.
        print "Couldn't open output file."
        return 1

    print "Successful write!"
    return 0

if __name__ == '__main__':
    main()
