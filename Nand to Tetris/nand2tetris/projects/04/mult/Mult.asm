// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

    @i      // i = 0
    M = 0

    @R0     // x = R0
    D = M
    @x
    M = D

    @R1     // y = R1
    D = M
    @y
    M = D

    @R2
    M = 0  


(LOOP)
    @i
    D = M
    @y
    D = M-D
    @END
    D;JEQ

    @x
    D = M
    @R2
    M = M+D

    @i
    M = M+1

    @LOOP
    0;JMP

(END)
    @END
    0;JMP



// Pseudo-Code
// int i = 0
// int x = R0
// int y = R1

// (LOOP)
// if (i = y) goto END
//  result = result + x
//  i++
//  goto LOOP

// (END)
// R2 = result