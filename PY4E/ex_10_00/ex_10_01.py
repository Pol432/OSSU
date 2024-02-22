import string
file = open("romeo-full.txt")
counts = dict()

for line in file:
    line = line.translate(str.maketrans("","", string.punctuation)) #Getting rid of punctuation in the
    #file
    line = line.lower()
    words = line.split()
    for word in words:
        counts[word] = counts.get(word, 0) + 1

lst = list()
for key,val in list(counts.items()):
    lst.append((val,key))

lst.sort(reverse=True)

for key, val in lst[:10]:
    print(key, val)
