__author__ = 'E'
import os
import sys
from parse import *
from file_write import *


def main():
    #Check if there are enough input arguments.  If not, exit.
    #print os.listdir('~/../VMs')
    if len(sys.argv) <2:
        print "Please enter appropriate command line arguments."
        return 1
    files_to_process = []
    directory = ""
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

    if len(files_to_process) == 1:
        content = parser_file(files_to_process[0])
        write_to_file(files_to_process[0], content)

    else:
        for i in files_to_process:
            content = parser_file(directory + "/" + i)
            write_to_file(i, content, directory)

    return 0

if __name__ == '__main__':
    main()
