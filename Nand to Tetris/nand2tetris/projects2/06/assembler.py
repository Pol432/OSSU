import sys
import os

class Assembler:
    def __init__(self, filename):
        self.file = open(filename + ".asm", "r")
        self.filename = filename
        self.pre = filename + "Pre.asm"
        self.sym = filename + "Sym.asm"
        self.JMP = ["null", "JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP"]
        self.COMP = {
                "0": "101010",
                "1": "111111",
                "-1": "111010",
                "D": "001100",
                "X": "110000",
                "!D": "001101",
                "!X": "110001",
                "-D": "001111",
                "-X": "110011",
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
        self.LABELS = {"SP": '0', "LCL": '1', "ARG": '2', "THIS": '3', "THAT": '4', "R0": '0', "R1": '1', "R2": '2', "R3": '3', "R4": '4', "R5": '5', "R6": '6', "R7": '7', "R8": '8', "R9": '9', "R10": '10', "R11": '11', "R12": '12', "R13": '13', "R14": '14', "R15": '15', "SCREEN": '16384', "KBD": '24576'}
        
        self.preprocess()
        self.symbol()
        self.parse()
        
        os.remove(self.sym)
        os.remove(self.pre)


    def preprocess(self):
        preFile = open(self.pre, "a+")
        # Getting rid of comments
        for line in self.file:
            if line.startswith("//") or line.isspace(): continue
            notComLine = line       # Not commented line
            if "//" in line:
                notComLine = line.split("//")[0]
            
            preFile.write(notComLine.strip() + "\n")
            
        preFile.close()


    def symbol(self):
        preFile = open(self.pre, "r")
        symFile = open(self.sym, "w")
        lines = preFile.readlines()
        newLines = []
        
        jumps = self.jumps()
        varCount = 16
        variables = {}
        
        for i in range(len(lines)):
            line = lines[i].strip()
            
            if line[0] == "(" or line == " " or line == "\n": continue

            elif line[0] == "@" and line[1].isalpha():
                cur = line[1:].strip()
                
                if cur in self.LABELS:
                    newLines.append("@" + self.LABELS[cur] + "\n")
                elif cur in jumps:
                    newLines.append("@" + jumps[cur] + "\n")
                elif cur in variables:
                    newLines.append("@" + variables[cur] + "\n")
                else:
                    variables[cur] = str(varCount)
                    varCount += 1
                    newLines.append("@" + variables[cur] + "\n")
            else:    
                newLines.append(line + "\n")
        
        symFile.writelines(newLines)
        symFile.close()
        
    
    def jumps(self):
        preFile = open(self.pre, "r")
        count = 0
        jumps = {}
        
        for line in preFile:
            if line[0] == "(":
                jumps[line[1:-2]] = str(count)
            else:
                count += 1
                
        preFile.close()     
        return jumps
    
    
    def parse(self):
        preFile = open(self.sym, "r")
        asm = open(self.filename + ".hack", "w")
        
        for line in preFile:
            if line.startswith("@"):
                ins = self.AInstruction(line)
            else:
                ins = self.CInstruction(line)
            asm.write(ins + "\n")

        preFile.close()
        asm.close()
            
            
    def AInstruction(self, ins):
        addr = ins.strip()[1:]
        return bin(int(addr))[2:].zfill(16)
    

    def CInstruction(self, ins):
        if ";" in ins:
            splIns = ins.split(";")
            jmp = bin(self.JMP.index(splIns[1].strip()))
            jmp = jmp[2:].zfill(3)
            comp = splIns[0].strip()
            comp = self.compParse(comp)
            res = "111" + comp + "000" + jmp
        else:
            splIns = ins.split("=")
            comp = self.compParse(splIns[1])
            dest = self.destParse(splIns[0])
            res = "111" + comp + dest + "000"
        
        return res
            

    def compParse(self, line):
        ins = line.replace(" ", "")
        if "M" in line: 
            a = "1"
            ins = ins.replace("M", "X")
        else:
            a = "0"
            ins = ins.replace("A", "X")
        return a + self.COMP[ins.strip()]
            


    def destParse(self, ins):
        d1 = d2 = d3 = "0"
        if "A" in ins: d1 = "1"
        if "D" in ins: d2 = "1"
        if "M" in ins: d3 = "1"
        return d1 + d2 + d3
        


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python assembler.py FILE.asm")
    
    filename = sys.argv[1].split('.')[0]
    
    Assembler(filename)
    
            

if __name__ == '__main__':
    main()