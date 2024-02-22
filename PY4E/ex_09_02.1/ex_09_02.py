file = input("Enter file name: ")
try:
    file = open(file)
except:
    print("Invalid file name", )
    quit()

counts = dict()
for line in file:
    line = line.rstrip()
    if line.startswith("From "):
        words = line.split()
        for word in words:
            counts[words[2]] = counts.get(words[2],0) + 1

print(counts)
