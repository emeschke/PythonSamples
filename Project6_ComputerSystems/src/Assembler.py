__author__ = 'Eric Meschke'

import sys
from Strip_line import *
from Parser import *
from Code import *
from SymbolTable import *

#Get the name of the file including the file path or return None if the file doesn't end with ".asm".
def get_file_name(input):
    #Check that the end of the file ends with .asm, if not return None
    if input[-4::] != '.asm':
        return None
    #Return the string minus the .in at the end of the file name.
    else:
        return input[0:-4]


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
        print "Input file is not valid, does not end with .asm extension.  No output written."
        return 1
    else:
        output += ".hack"

    #Try to open the input file and read in the contents.  If it won't open print error and exit.  Using with/open has
    #the advantage of closing the file after the suite finishes.
    try:
        with open(str(sys.argv[1])) as inputFile:
            content = inputFile.readlines()
    except IOError:
        print "Input file not found.  Please check the path and filename and try again."
        return 1

    #Lists for the different stages of translation.
    clean_content = []          #Cleaned lines
    parsed_content = []         #Parsed lines into pneumonics
    translated_content = []     #Translated lines

    #Clean the input from file by removing comments and whitespace.  Store in a list.
    for i in content:
        #Remove_comments; strip the line.
        i = remove_comments(i)
        i = strip_line(i)
        #If the entire line is a new line then it is a blank line, don't prin.  Also check for the
        # carriage return in linux which is \r rather than \n
        if i == '\n' or i == '\r' or i == '\r\n' or len(i) == 0:
            pass
        else:
            clean_content.append(i)

    #Create a new symbol table object.
    symbol_table = SymbolTable()

    #Run through the lines of the program to build the dictionary of memory addresses.  Count the number of lines
    #and also keep track of how many lines are L-commands and subtract that off.
    counter = 0
    removed = 0
    for i in clean_content:
        if i[0] == '(':
            #Add the symbol to the symbol table.
            symbol_table.add_mem_address(i[1:-1], counter-removed)
            removed +=1
        counter +=1

#This was code to take out L-commands, but it didn't work reliably.  Handled below.
#    for i in clean_content:
#        if i[0] == '(' or i[-1] == ')':
#            clean_content.remove(i)

    #Return a list of lists, one for each line, that represent each line after it is symbol handled.
    for i in clean_content:
        #Skip L-commands.
        if i[0] == '(':
            pass
        #If i is an A instruction that is not digits, try to add the symbol to the symboltable.  Then look up the
        #proper address and substitute it.
        elif i[0] == '@' and i[1::].isdigit() is not True:
            symbol_table.add_mem_address(i[1::])
            new_i = "@" + str(symbol_table.get_mem_address(i[1::]))
            parsed_list = parser(new_i)
            parsed_content.append(parsed_list)
        #Else line is symbol-less so handle it normally.
        else:
            parsed_list = parser(i)
            parsed_content.append(parsed_list)

    #For each list (representing a line) get the binary representation of the line.
    for i in parsed_content:
        this_line = get_bin(i)
        translated_content.append(this_line)

    #Try to open the output file.  Because it will create/overwrite there should be no problem with opening it, but
    #still good practice to handle the exception.  Write the binary representation to the file.
    try:
        with open(output, "w") as outputFile:
            print "Files opened successfully."
            #for i in translated_content:
            for i in translated_content:
                outputFile.writelines(i + "\n" )

    except IOError:
        #If it couldn't print to output, exit.
        print "Couldn't open output file."
        return 1

    print "Successful write!"
    return 0

if __name__ == '__main__':
    main()