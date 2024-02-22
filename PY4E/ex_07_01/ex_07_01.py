file = open("mbox-short.txt")

for line in file:
    upperlin = line.upper()
    upperlin = upperlin.strip()
    print(upperlin)
