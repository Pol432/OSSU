"""
Virtual Machine Translator program (Translates Virtual Machine Language Files into Assembly Language)
Usage: >python VMTranslator.py VMFILENAME.vm
"""

import sys
import os

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: >python VMTranslator.py VMFILENAME.vm")
        
    vmFile = open(sys.argv[1], "r")
    
    global vmFileName
    vmFileName = ((sys.argv[1]).split("."))[0]                      # Getting the original file's name
    asmFile = open(vmFileName + ".asm", "w")

    """ """
    for line in vmFile:
        line = line.strip()
        
        if line.startswith("//") or (not line.strip()):             # Empty lines and comments
            continue
        
        ins = (line.split("//")[0]).strip()                         # Getting rid of comments in the instruction
        insArg0 = (ins.split()[0]).strip()
        
        
        
        asmFile.write("//" + ins + "\n")
        # Case for Arithmetic instructions
        if insArg0 in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            arthTran = globals()[insArg0 + "Tr"]()                  # Arithmetic translation
            asmFile.write(arthTran)
            
        # Case for Memory instructions
        elif insArg0 in ["pop", "push"]:
            if insArg0 == "pop":
                popTran = popTr(str(ins))
                asmFile.write(popTran)
            else:
                pushTran = pushTr(str(ins))
                asmFile.write(pushTran)
    
    asmFile.write("(END_OF_PROGRAM)\n@END_OF_PROGRAM\nD;JMP")
    
    
    vmFile.close()
    asmFile.close()


""" Assembly Code Instructions """
atSP  = "@SP\nA=M\n"        # *SP
redSP = "@SP\nM=M-1\n"      # SP--
incSP = "@SP\nM=M+1\n"      # SP++


""" ARITHMETIC TRANSLATORS"""
def addTr():
    return redSP + atSP + "D=M\n" + redSP + atSP + "M=M+D\n" + incSP

def subTr():
    return redSP + atSP + "D=M\n" + redSP + atSP + "M=M-D\n" + incSP

def negTr():
    return redSP + atSP + "M=-M\n" + incSP

def eqTr():
    sub = subTr()                                       # Substracting first two numbers in stack (if x=y then x-y = 0)
    return logicalTr(sub,"EQ")

def gtTr():
    sub = subTr()                                       # Substracting first two numbers in stack (if x=y then x-y > 0)
    return logicalTr(sub,"GT")

def ltTr():
    sub = subTr()                                       # Substracting first two numbers in stack (if x=y then x-y > 0)
    return logicalTr(sub,"LT")

def andTr():
    falseCase = "@FALSE_CASE" + "D;JNE\n"               # If *sp is true, then *sp-1=0 so jump to False Case if not
    return redSP + atSP + "D=M-1\n" + falseCase + redSP + atSP + "D=M-1\n" + falseCase + atSP + "M=1\n" + "@REST_CODE" + "D;JMP" + "(FALSE_CASE)" + atSP + "M=0\n" + "(REST_CODE)\n" + incSP

def orTr():
    trueCase = "@TRUE_CASE" + "D;JEQ\n"
    return redSP + atSP + "D=M-1\n" + trueCase + redSP + atSP + "D=M-1\n" + trueCase + atSP + "M=0\n" + "@REST_CODE" + "D;JMP" + "(TRUE_CASE)" + atSP + "M=1\n" + "(REST_CODE)\n" + incSP

def notTr():
    return redSP + atSP + "M=!M" + incSP

""" Function that traduces eq, gt & lt operations """
def logicalTr(sub, operation):
    skip = "@REST_CODE\n" + "D;JMP\n"
    return sub + redSP + atSP + "D=M\n" + "@TRUE_CASE\n" + "D;J" + operation + "\n" + atSP + "M=0\n" + skip + "(TRUE_CASE)\n" + atSP + "M=1\n" + "(REST_CODE)\n"



""" MEMORY TRANSLATORS """
symbols = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT"     
    
}
def pushTr(ins):
    ins = ins.split()
    segmentPointer = ins[1].strip()
    i = ins[2]
    
    if segmentPointer in symbols:                                       # Case for local, argument, this, that
        addr = "@" + i + "\n" + "D=A\n" + "@" + symbols[segmentPointer] + "\n" + "A=M+D\n" + "D=M\n"
        return addr + atSP + "M=D\n" + incSP

    elif segmentPointer == "constant":                                  # Case for constant
        i = "@" + i + "\n" + "D=A\n"
        return i + atSP + "M=D\n" + incSP
    
    elif segmentPointer == "temp":                                      # Case for temp
        i = int(i) + 5   
        addr = "@" + str(i) + "\n"
        return addr + "D=M\n" + atSP + "M=D\n" + incSP
    
    elif segmentPointer == "pointer":                                   # Case for pointer
        thisOrThat = {"0": "THIS", "1": "THAT"}
        i = thisOrThat[str(i)]
        addr = "@" + i + "\n" + "D=M\n" 
        return addr + atSP + "M=D\n" + incSP
    
    elif segmentPointer == "static":                                    # Case for static
        addr = "@" + vmFileName + "." + i + "\n" + "D=M\n"
        return addr + atSP + "M=D\n" + incSP
    
    

addrCounter = 0
def popTr(ins):
    ins = ins.split()
    segmentPointer = ins[1].strip()
    i = ins[2].strip()
    
    if segmentPointer in symbols:                                       # Case for local, argument, this, that
        global addrCounter
        addr = "@" + i + "\n" + "D=A\n" + "@" + symbols[segmentPointer] + "\n" + "D=M+D\n"
        atAddr = "@addr" + str(addrCounter) + "\n"
        addrCounter += 1
        return redSP + addr + atAddr + "M=D\n" + atSP + "D=M\n" + atAddr + "A=M\n" + "M=D\n"
    
    elif segmentPointer == "temp":                                      # Case for temp
        i = int(i) + 5
        addr = "@" + str(i) + "\n"
        return redSP + atSP + "D=M\n" + addr + "M=D\n"
    
    elif segmentPointer == "pointer":                                   # Case for pointer
        thisOrThat = {"0": "THIS", "1": "THAT"}
        i = thisOrThat[str(i)]
        addr = "@" + i + "\n"
        return redSP + atSP + "D=M\n" + addr + "M=D\n"
    
    elif segmentPointer == "static":                                    # Case for static
        addr = "@" + vmFileName + "." + i + "\n" + "M=D\n"
        return redSP + atSP + "D=M\n" + addr



if __name__ == "__main__":
    main()