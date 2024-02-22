
days = dict()
file = input("Enter the file name: ")
count = 0
max = 0
maxN = dict()

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
            if i == lineA[1]:
                days[i] = days.get(i, 0) + 1

#print(days)

for i,value in days.items():
    count = int(value)
    #print(count)
    if count > max:
        maxN = i,value
        max = count
    #print(value)


print(type(maxN))
print(maxN[0], end = " ") 
print(maxN[1])
