"""
Hack assembler program (Translates Hack Assembly Language Files into Machine Language)
Usage: >python HackAssembler.py HACKFILENAME.asm
"""

import sys
import os

variablesDict = {
    "@SCREEN": "@16384",
    "@KBD": "@24576",
    "@SP": "@0",
    "@LCL": "@1",
    "@ARG": "@2",
    "@THIS": "@3",
    "@THAT": "@4"
}

""" Main method """
def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: >python HackAssembler.py HACKFILENAME.asm")
        
    asmFile = open(sys.argv[1], "r")
    
    newFileName = ((sys.argv[1]).split("."))[0]                 # Getting the original file's name
    
    firstFile = open(newFileName + ".first", "w")               # First pass file
    
    # First writting a text file without symbols
    """ First Pass (Label and Pre-defined symbols) """
    instructionCount = 0
    
    for line in asmFile:
        line = line.strip(" ")
        
        if line.startswith("//") or (not line.strip()):         # Empty line
            continue
        
        temp = line.strip("\n\t ")
        temp = temp.split()[0]
        ins = str(temp.split("//")[0])                          # Getting only the original instruction without any comments or whitespaces
        
        isPreDefined = inPreDefined(ins)                        # Check if instruction is a pre-defined symbol  
        if isPreDefined:                     
            firstFile.write(isPreDefined + "\n")
            instructionCount += 1
            continue
        
        isLabel = inLabel(ins, instructionCount)                # Check for labels
        if isLabel:                       
            continue
        
        else:
            instructionCount += 1
            firstFile.write(line)
            
                
    
    """ Second Pass (Variable Symbols)"""
    firstFile.close()
    firstFile = open(newFileName + ".first", "r")   
    secondFile = open(newFileName + ".second", "w")                 # Second pass file
    currentMemory = 16
    
    for line in firstFile:    
        if line.startswith("@") and line[1].isalpha():              # Check if line is a variable
            currentVar = line.strip("@ \n")
            
            if currentVar in variablesDict:                         # Case for already added variable
                value = variablesDict[currentVar]
                secondFile.write("@" + str(value) + "\n")
            else:                                                   # Case for new variable
                secondFile.write("@" + str(currentMemory) + "\n")
                variablesDict[currentVar] = currentMemory
                currentMemory += 1
                
        else:
            secondFile.write(line)
            
    
    firstFile.close()
    os.remove(newFileName + ".first")
    
    
    """ Final Pass (Changing code to binary) """
    secondFile.close()
    secondFile = open(newFileName + ".second", "r")  
    hackFile = open(newFileName + ".hack", "w")
    
    for line in secondFile:
        if line.startswith("@"):                                # A Instruction
            aIns = (line.split("@"))[1]
            aBinary = A_InsToBinary(str(aIns))
            hackFile.write(aBinary + "\n")
            
        else:                                                   # C Instruction
            if "//" in line:                                    # Checking for comments
                cIns = line.split("//")[0]      
                cBinary = C_InsToBinary(cIns.strip())
                hackFile.write(cBinary + "\n")
            else:
                cIns = line.strip()
                cBinary = C_InsToBinary(cIns)
                hackFile.write(cBinary + "\n")
                
    
    asmFile.close()
    hackFile.close()
    secondFile.close()
    os.remove(newFileName + ".second")


""" 
----- Pre-Defined Symbol Checker ----
Helper function that takes an instruction and returns false if given instruction isn't a symbol. 
Otherwise, returns the non-symbolic form of the instruction.
"""
def inPreDefined(ins):                                  
    if ins in variablesDict:                   # Case for pre-defined symbol which is not a register
        return variablesDict[ins]
    
    elif ins.startswith("@R") and ins[2].isdigit():                 # Case for Register symbol
        regNum = ins.split("@R")[1]
        return "@" + str(regNum)
    
    else:
        False


""" 
----- Label Checker -----
Helper function that takes an instruction and returns false if given instruction isn't a label.
Otherwise, adds label in the variable's dictionary and returns true.
"""
def inLabel(ins, instructionCount):
    onlyIns = ins.strip("@")                    
    
    if onlyIns.startswith("(") and onlyIns.endswith(")"):
        label = onlyIns.strip("()")
        variablesDict[label] = str(instructionCount)
        return True
    
    else:
        return False


""" A Instruction """ 
def A_InsToBinary(value):
    val = str(bin(int(value))[2:])   # Returning binary form of the value withour 0b
    return val.rjust(16, "0")   # Filling gaps with 0
        

""" C Instruction """
def C_InsToBinary(value):
    isDest = False
    isJump = False
    
    if "=" in value:
        sepValue = value.split("=")
            
        destValue = destToBinary(sepValue[0].strip())
        compValue = compToBinary(sepValue[1].strip())
            
        isDest = True
            
    if ";" in value:
        sepValue = value.split(";")
            
        jumpValue = jumpToBinary(sepValue[-1].strip())
        compValue = compToBinary(sepValue[-2].strip())
            
        isJump = True
            
    if (not isDest) and (not isJump):
        compValue = compToBinary(value)
            
    if not isDest:
        destValue = "000"
    if not isJump:
        jumpValue = "000"
            
    return "111" + str(compValue) + str(destValue) + str(jumpValue)
            

compDict = {
    "0" : "101010",
    "1" : "111111",
    "-1": "111010",
    "D" : "001100",
    "X" : "110000",
    "!D": "001101",
    "!X": "110001",
    "-D": "001111",
    "-": "110011",
    "D+1": "011111",
    "X+1": "110111",
    "D-1": "001110",
    "X-1": "110010",
    "D+X": "000010",
    "D-X": "010011",
    "X-D": "000111",
    "D&X": "000000",
    "D|X": "010101"
}
def compToBinary(value):
    if "A" in value:
        noAValue = value.replace("A", "X")
        return "0" + str(compDict.get(noAValue))
    elif "M" in value:
        noMValue = value.replace("M", "X")
        return "1" + str(compDict.get(noMValue))
    else:
        return "0" + str(compDict.get(value))

def destToBinary(value):
    d1 = int("A" in value)
    d2 = int("D" in value)
    d3 = int("M" in value)
        
    return str(d1) + str(d2) + str(d3)
    
jumpList = ["null", "JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP"]
def jumpToBinary(value):
    if value not in jumpList:
        return "000"
    index = bin(jumpList.index(value))[2:]
    return index.rjust(3, "0")



if __name__ == "__main__":
    main()