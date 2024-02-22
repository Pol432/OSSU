file = input("Enter your file name: ")
try:
    file = open(file)
except:
    print("Invalid file name:", file)
    quit()

dnd = dict() #Creating a domain name dictionary to save those names

for line in file:
    if line.startswith("From: "):
        line = line.rstrip()
        dname = line.split("@")
        dnd[dname[1]] = dnd.get(dname[1],0) + 1

print(dnd)
