Eric Meschke, Homework 7, CSPP52011

The package to complete project 7 includes the following files: VM1.py, parse.py, file_write.py, Readme.txt and
Assembly.txt.  The syntax to use the program is one of the following:
$python VM1.py <filename>.asm
$python VM1.py <directory>

The program is guaranteed to work in both windows and Linux (CS dept servers) using this syntax when the file to read
is in the same directory as VM1.py, when the directory is a sub-directory of the directory where VM1.py resides, and
when the directory is the directory where VM1.py resides.

Because of portability issues between Windows and Linux and the difference in file structure between '/' and '\' it
is not guaranteed to work on a general file/directory input whose path is more complicated.

****Important--this may not be completely general for all paths but it should be pretty easy to generate .asm files.
Please let me know if you can't easily get it to work.

The module functions are as follows:
VM1.py--Calls the main function.  Does input validation of the command line and calls function to open/read file, and
to translate it and write to file.  Iterates over all files input if the command line input is a directory.

parse.py--A set of functions to strip whitespace and return the each line in the format of a ist [arg1, arg2, arg3]

file_write.py--Set of function to translate each type of command and write it to the filename supplied.

Modules are further documented within the code.  An explanation of the assembly language for each command is in 
assembly.txt.

All files work correctly and a VMs directory is included.  It includes VMs that were the dry test cases as well as 
the corresponding .asm files that were generated.  The .asm files work correctly in the CPUemulator.