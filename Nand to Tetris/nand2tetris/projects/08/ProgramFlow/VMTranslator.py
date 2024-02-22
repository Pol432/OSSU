"""
Virtual Machine Translator program (Translates Virtual Machine Language Files into Assembly Language)
Usage: >python VMTranslator.py VMFILENAME.vm
"""

import sys
import os

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: >python VMTranslator.py VMDIRECTORY")
        
    vmName = sys.argv[1]
    
    global asmFile
    asmFile = open(str(sys.argv[1]).strip(" .vm") + ".asm", "w")
    
    
    if vmName.endswith("vm"):
        global vmFileName
        vmFileName = vmName.split(".")[0]
        
        vmFile = open(vmName, "r")
        fileTran(vmFile)
    
    else:
        asmFile.write(initP())
        vmDirectory = vmName
        for filename in os.listdir(vmDirectory):
            if filename.split(".")[1].strip() == "vm":
                vmFile = open(os.path.join(vmDirectory, filename), 'r')
                
                vmFileName = filename.split(".")[0]
                fileTran(vmFile)
            
            

    asmFile.close()

""" VM File Translator """
def fileTran(vmFile):
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
                
        # Case for Branching instructions
        elif insArg0 in ["label", "goto", "if-goto"]:
            branchTran = branchTr(str(ins))
            asmFile.write(branchTran)
                    
        elif insArg0 in ["function", "call", "return"]:
            funTran = funTr(ins)
            asmFile.write(funTran)
            
    vmFile.close()



""" Assembly Code Instructions """
atSP  = "@SP\nA=M\n"        # *SP
redSP = "@SP\nM=M-1\n"      # SP--
incSP = "@SP\nM=M+1\n"      # SP++

atCounter = 0
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
    return redSP + atSP + "D=M\n" + redSP + atSP + "M=D&M\n" + incSP

def orTr():
    return redSP + atSP + "D=M\n" + redSP + atSP + "M=D|M\n" + incSP

def notTr():
    return redSP + atSP + "M=!M\n" + incSP

""" Function that traduces eq, gt & lt operations """
def logicalTr(sub, operation):
    global atCounter
    atRest = "@REST_CODE" + str(atCounter) + "\n"
    labelRest = "(REST_CODE" + str(atCounter) + ")\n"
    skip = atRest + "D;JMP\n"
    
    atCounter += 1
    return sub + redSP + atSP + "D=M\n" + "@TRUE_CASE" + str(atCounter) + "\nD;J" + operation + "\n" + atSP + "M=0\n" + skip + "(TRUE_CASE" + str(atCounter) + ")\n" + atSP + "M=-1\n" + labelRest + incSP



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
    

varCounter = 0
def popTr(ins):
    ins = ins.split()
    segmentPointer = ins[1].strip()
    i = ins[2].strip()
    
    if segmentPointer in symbols:                                       # Case for local, argument, this, that
        addr = "@" + i + "\n" + "D=A\n" + "@" + symbols[segmentPointer] + "\n" + "D=M+D\n"
        return redSP + addr + "@R13\n" + "M=D\n" + atSP + "D=M\n" + "@R13\n" + "A=M\n" + "M=D\n"
    
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


""" BRANCHING TRANSLATOR """
def branchTr(ins):
    ins = ins.split()
    label = ins[1].strip()
    atLabel = "@" + label + "\n"
    ins = ins[0].strip()
    
    if ins == "label":
        return "(" + label + ")\n"
    
    if ins == "goto":
        trans  = atLabel
        trans += "0;JMP\n"
        return trans
    
    if ins == "if-goto":
        trans  = redSP
        trans += atSP
        trans += "D=M\n"
        trans += atLabel
        trans += "D;JNE\n"
        return trans
    
    
""" FUNCTION TRANSLATOR """
def funTr(ins):
    ins = ins.split()
    command = ins[0].strip()
    
    if command == "return":
        trans  = "@LCL\n"
        trans += "D=M\n"
        trans += "@R15\n"
        trans += "M=D\n"
        trans += "@5\n"
        trans += "D=A\n"
        trans += "@R15\n"
        trans += "D=M-D\n"
        trans += "A=D\n"
        trans += "D=M\n"
        trans += "@R14\n"
        trans += "M=D\n"
        trans += popTr("pop argument 0")
        trans += redSP
        trans += "@ARG\n"
        trans += "D=M\n"
        trans += "@SP\n"
        trans += "M=D+1\n"
        for i in range(1,5):
            trans += restore(i)
        trans += "@R14\n"
        trans += "A=M\n"
        trans += "0;JMP\n"
        return trans
    
    funName = ins[1].strip()
    n = ins[2].strip()

    if command == "function":
        trans = "(" + funName + ")\n"
        trans += "@0\n"
        trans += "D=A\n"
        for i in range(int(n)):
            trans += atSP + "M=D\n" + incSP
        return trans
        
    if command == "call":
        global varCounter
        trans  = "@returnAddress" + str(varCounter) + "\n"
        trans += "D=A\n"
        trans += atSP
        trans += "M=D\n"
        trans += incSP
        for i in range(1,5):
            trans += pushCaller(i)
        trans += "@5\n"
        trans += "D=A\n"
        trans += "@SP\n"
        trans += "D=M-D\n"
        trans += "@" + n + "\n"
        trans += "D=D-A\n"
        trans += "@ARG\n"
        trans += "M=D\n"
        trans += "@SP\n"
        trans += "D=M\n"
        trans += "@LCL\n"
        trans += "M=D\n"
        trans += branchTr("goto " + funName + "\n")
        trans += "(returnAddress" + str(varCounter) + ")\n"
        
        varCounter += 1
        return trans

restoreDict = {"1": "THAT", "2": "THIS", "3": "ARG", "4": "LCL"}
def restore(n):
    n = str(n)
    trans  = "@" + n + "\n"
    trans += "D=A\n"
    trans += "@R15\n"
    trans += "D=M-D\n"
    trans += "A=D\n"
    trans += "D=M\n"
    trans += "@" + restoreDict[n] + "\n"
    trans += "M=D\n"
    return trans

pushDict = {"1": "LCL", "2": "ARG", "3": "THIS", "4": "THAT"}
def pushCaller(n):
    n = str(n)
    trans  = "@" + pushDict[n] + "\n"
    trans += "D=M\n"
    trans += atSP
    trans += "M=D\n"
    trans += incSP
    return trans

def initP():
    tran  = "@256\n"
    tran += "D=A\n"
    tran += "@SP\n"
    tran += "M=D\n"
    tran += "D=-1\n"
    tran += "@LCL\n"
    tran += "M=D\n"
    tran += "@LCL\n"
    tran += "M=D\n"
    tran += "@ARG\n"
    tran += "M=D\n"
    tran += "@THIS\n"
    tran += "M=D\n"
    tran += "@THAT\n"
    tran += "M=D\n"
    tran += funTr("call Sys.init 0")
    return tran

if __name__ == "__main__":
    main()