The Assembler program works using python 2.7 in both windows and linux on the computers in the CS department.  Syntax
from the command prompt in bash is $python Assembler.py <filename>.asm.  The program reads in a .asm file and outputs
a .hack file.  There are no known bugs in the program.  All files were translated from machine to assembly successfully,
the results are stored in Asms sub-directory.

The following modules/.py files must be included in the directory in order for the program to work.  Their high level
construction is detailed below.
Assembler.py
Code.py
Parser.py
Strip_line.py
SymbolTable.py

There are four modules that are used in the code in addition to the Assembler file, which has the main function.

--Strip_line: Has two functions, one to remove comments and one to remove white space. Input/return are strings.
--Parser: Input is a string.  Parser returns a list[5] = [command_type, symbol, dest, comp, jump].  If the command type
doesn't have a certain input (ie A-command has no dest/comp/jump) the field is left blank.  Each field corresponds to
a function and a function parser aggregates the results and returns the list.
--Code: Reads in a list [5] of the format output by Parser.  Defined in the module are python style dictionaries
(same as hash tables) that correspond to each input and the binary value associated.  The dictionaries are declared
for dest, acomp, notacomp and jump.  The module looks up and concatenates the correct values from the input list using
the dictionaries.  The binary representation is returned.
--SymbolTable is a class that represents a symbol table.  In its constructor a dictionary is initiated with the program
defined inputs.  There is a method to add members to the dictionary and a method to get a value from the dictionary
when a key is provided.

Assembler handles the main function.  It handles the opening and writing to the file, including input checking for the
sysargs.  Within main it handles the cleaning, population of the symbol table, parsing of the line, and conversion
to binary using the modules detailed above and the SymbolTable class.  All documented within the Assembler file.


