// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

//Set the MIN pixel value
@16384     //Set A to the value of the first pixel
D=A        //Set D to A
@MIN       //Initialize register for MIN
M=D        //Set the value of RMIN to first pixel.

//Same process for a MAX pixel
@24575     //Set A to the value of last pixel
D=A        //Set D to A
@MAX       //Initialize register for MAX
M=D        //Set the value of RMAX to first pixel.

//Set counter to the MIN value.
@MIN       //Set A to RMIN
D=M        //Set D to the value of MIN pixel
@COUNTER   //Set A to RCOUNTER
M=D        //Set the value of RCOUNTER to D (MIN)

//Check value of keyboard input.  Two branches--either increment the counter //and change that memory address (pixel) to -1 (black) or decrement the //counter and change the memory address (pixel) to 0--depends on keyboard //input.  Only perform the increment/decrement after checking that the //min/max hasn't been reached.

//If/else statement after the counter value is checked.
(LOOP)
@24576     //Set A to Keyboard input address
D=M        //Set D to the COUNTER value
@NOKEY     //NOKEY code line number
D;JEQ      //Jump to NOKEY line if key is pressed
@KEY       //KEY code line number
D;JNE      //Jump to KEY line if key is not pressed

(NOKEY)    
@COUNTER   //Set A to COUNTER address
D=M	   //Get counter value from memory
@MIN       //Set A to MIN address
D=D-M      //Find difference between D and MIN
@LOOP      //Set A to LOOP line
D;JEQ      //Jump to LOOP if the COUNTER and MIN are equal
@COUNTER   //Set A to COUNTER address
M=M-1      //Decrement the COUNTER
A=M        //Set the memory address to M, the value of COUNTER
M=0        //Set the memory address of the COUNTER to 0, un-darkening it.
@LOOP      //Set the line to LOOP
0;JMP      //Jump to LOOP

(KEY)
@COUNTER   //Set A to COUNTER address
D=M	   //Get counter value from memory
@MAX       //Set A to MAX address
D=D-M      //Find difference between D and MAX
@IFMAX      //Set A to LOOP line
D;JEQ      //Jump to LOOP if the COUNTER-MAX == 0
@COUNTER   //Set A to COUNTER address
A=M        //Set A to the to COUNTER value
M=-1       //Set the address stored in COUNTER to -1, darkening it.
@COUNTER   //Set A to the COUNTER value
M=M+1      //Increment the COUNTER
@LOOP      //Set the line to LOOP
0;JMP      //Jump to LOOP

(IFMAX)    //Because the Counter exits if Max=counter, the last square never gets filled in.
@MAX       //This loop takes care of that problem by manually filling it in every time
A=M        //the if statment where max=counter trips.
M=-1
@LOOP
0;JMP
   