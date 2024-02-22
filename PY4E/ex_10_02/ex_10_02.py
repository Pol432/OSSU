file = input("Enter a file name: ")
try:
    file = open(file)
except:
    print("File couldn't be oppened: ", file)
    quit()

hCount = dict()
for line in file:
    if line.startswith("From "):
        words = line.split()
        hours = words[5].split(":")
        hCount[hours[0]] = hCount.get(hours[0],0) + 1

fCount = list()
for hour,count in hCount.items():
    fCount.append((hour,count))

fCount.sort()#(reverse=True)

for hour,count in fCount:
    print(hour, count)
