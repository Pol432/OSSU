
hours = dict()
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
            if i == lineA[5]:
                hoursA = dict()
                hoursA = lineA[5]
                hoursA = hoursA.split(":")
                for i in hoursA:
                    if i == hoursA[0]:
                        hours[i] = hours.get(i, 0) + 1
                        #print(hours)
                        #quit()


#print(hours)
list = list()
for i,v in hours.items():
    maxN = (i,v)
    list.append(maxN)

list = sorted(list)

for v,i in list:
    print(v,i)


#for i,value in hours.items():
    #count = int(value)
    #print(count)
    #if count > max:
        #maxN = i,value
        #max = count
    #print(value)


#print(type(maxN))
#print(maxN[0], end = " ")
#print(maxN[1])
