words = list()
file = open("romeo.txt", "r")

for line in file:
    words_in_line = line.split()
    for word in words_in_line:
        if word in words:         continue
        words.append(word)

words.sort()
print(words)
