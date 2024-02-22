import sys
import os


class Compiler:
    def __init__(self, file):
        self.fname = file.split(".")[0]
        self.pre = None
        self.infile = open(file, "r")
        self.tab = 1
        
        self.preprocess()
        #self.analizer()

    
    def analizer(self):
        self.pre = open(self.fname + "Pre.jack", "r")
        with open(self.fname + ".xml", "w") as xmlFile:
            self.line = self.pre.readline()
            while self.line:
                if self.line.startswith("class"):
                    self.tokClass()
                
                self.line = self.pre.readline()
                
    
    def tabWriter(self):
        tab = ""
        for i in range(self.tabs):
            tab += "\t"
        return tab
         
    
    def tokClass(self):
        1
    
    def isComment(self, line):
        double = line.startswith("//")
        return (line.startswith("/*") and line.endswith("*/")) or (line.startswith("/**") and line.endswith("*/")) or double
    
    def preprocess(self):
        preFile = open(self.fname + "Pre.jack", "w")
        inComment = False
        
        for line in self.infile:
            # Ignore line that belongs to a comment: is in between /*** */ or /* */
            if inComment:
                if line.startswith("*/") or line.endswith("*/"):
                    inComment = False
                    continue
                else: continue

            if line.isspace() or self.isComment(line.strip()):
                continue
            elif line.startswith("/*"): 
                inComment = True
                continue
            notComLine = line
            if "//" in line:
                notComLine = line.split("//")[0]
                
            preFile.write(notComLine) 
        
        preFile.close()
        self.infile.close()

        

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python compiler.py FILE.jack|DIR")

    input_path = sys.argv[1]
    
    if os.path.isfile(input_path):
        # If the input is a file
        filename = os.path.splitext(input_path)[0]
        Compiler(filename + ".jack")
        
    elif os.path.isdir(input_path):
        # If the input is a directory
        files = os.listdir(input_path)
        for file_name in files:
            if file_name.endswith(".jack"):
                Compiler(os.path.join(input_path, file_name))
    else:
        sys.exit("Invalid input: Please provide a valid file or directory path.")


if __name__ == '__main__':
    main()