from collections import Counter #Importing Counter to count the number of letters
import string
file = input("Enter a file name: ")
try:
    file = open(file)
except:
    print("File couldn't be oppened: ", file)
    quit()

counts = Counter() #Converting counts in a Counter dictionary

#Adding each character on each line on the counts dictionary without counting punctuation or newlines
for line in file:
    line = line.strip()
    line = line.lower()
    line = line.translate(str.maketrans("","", string.punctuation))
    counts += Counter(line)

#Adding each counts and letters on a tuple list so we can sort it and then print it
lCounts = list()
for i,u in counts.items():
    lCounts.append((i,u))

lCounts.sort()

for i,u in lCounts[12:]: #Printing from [12:] so we don't count numbers nor tabs nor white spaces
    print(i,u)
