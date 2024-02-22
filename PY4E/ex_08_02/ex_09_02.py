
days = dict()
file = input("Enter the file name: ")

try:
    file = open(file, "r")
except:
    print("That is not a valid file name!")
    quit()


for line in file:
    if line.startswith("From "):
        #print(line)
        lineA = line.rstrip()
        lineA = lineA.split()
        #print(lineA)
        for i in lineA:
            if i == lineA[2]:
                days[i] = days.get(i, 0) + 1

print(days)
                #quit()
