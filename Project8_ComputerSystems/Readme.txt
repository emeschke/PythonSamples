Eric Meschke, Homework 8, CSPP52011

The package to complete project 8 includes the following files: VM1.py, parse.py, file_write.py, Readme.txt and
Assembly.txt.  The syntax to use the program is one of the following:
$python VM1.py <filename>.asm <output_file>
$python VM1.py <directory> <output_file>
An option flag -bs (pun intended) can be appended as a fourth argument to add the bootstrap code.
$python VM1.py <input> <output> -bs

It is necessary to use the -bs argument in order to generate proper code for FibonacciSeries and StaticsTest.  It should
not be used for the simpler programs as the code in the tester is pre-loaded.

The program generates code that is testable for all the test cases.  Right now it doesn't work for FibonacciSeries or
StaticsTest.  There may be a bug in the implementation of call.  Will try to fix it and resubmit.  The three simpler
cases work fine when compared to the test script.  All files are included (.asm as well.)

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

