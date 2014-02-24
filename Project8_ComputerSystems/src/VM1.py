__author__ = 'E'
import os
import sys
from parse import *
from file_write import *


def main():
    #Check if there are enough input arguments.  If not, exit.  User must specify an input and an output.
    if len(sys.argv) <3:
        print "Please enter appropriate command line arguments."
        return 1
    files_to_process = []
    directory = ""
    output = sys.argv[2]
    # If the input from command line is a .vm file there is only one file to process.
    if sys.argv[1][-3::] == ".vm":
        files_to_process.append(sys.argv[1])
    #Otherwise it must be a directory to process.
    else:
    #Get all the files to process and put them in a list.
        #this is the home directory ('~/..')
        #Try/except to make sure it is a directory.  If it fails for any reason program exits.
        try:
            for i in os.listdir(sys.argv[1]):
                if i[-3::] == ".vm":
                    files_to_process.append(i)
            directory = sys.argv[1]

        except Exception:
            print "Not a valid directory input.\nExiting, please try again.\n"
            return 1

    print "Processing..."

    #If there is only one file to process, can use "generic" as the filename.  It is not used for writing, only for
    #tracking in the code for looping and jumping.

    #Remove the output file if it exists.  It will be re-created in append mode when the output is written to.
    if os.path.isfile(output):
        os.remove(output)

    if len(sys.argv) >= 4 and sys.argv[3] == "-bs":
        write_init(output)

    #If there is only one file, pass it with "generic."  This is a work around because it is hard to work with both
    #the input path and the input filename.
    if len(files_to_process) == 1:
        content = parser_file(files_to_process[0])
        write_to_file("generic", content, output)

    #Otherwise it is a directory, process through the list.
    else:
        for i in files_to_process:
            content = parser_file(directory + "/" + i)
            write_to_file(i, content, output)

    return 0

if __name__ == '__main__':
    main()