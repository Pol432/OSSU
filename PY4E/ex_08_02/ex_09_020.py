fhand = open('mbox-short.txt')
day = dict()
for line in fhand:
    if line.startswith('From '):
        line = line.rstrip()
        words = line.split()
        day[words[2]] = day.get(words[2],0) + 1
print(day)
