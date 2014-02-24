// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[3], respectively.)

@2         //Sets A to R2
M=0        //Sets the value of R2 to 0.

(LOOP)
@0         //Set A to R0
D=M        //Set D to the value in R0
@END       //Set A to the value of (END)
D;JLE      //If D<=0 , Jump to the end (infinte loop)
@1         //Set A to R1
D=M        //Set D to the value in R1
@2         //Set A to R2
M=D+M      //Add the value in R1 (D) to R2 value 
@0         //Decrement the value of R0
M=M-1      // i=i+1
@LOOP
0;JMP      // Goto LOOP
(END)
@END
0;JMP      // Infinite loop 