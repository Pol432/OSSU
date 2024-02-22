txt = "but soft what light in yonder window breaks"
t = list()
words = txt.split()
for word in words:
    t.append((len(word),word))

t.sort(reverse=True)

res = list()
for lengh, word in t:
    res.append(word)

print(res)
