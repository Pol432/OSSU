fname = input("Enter file name: ")
text = open(fname)
line_counter = 0
values = 0 #all float values summed here
for line in text:
    if line.startswith('X-DSPAM-Confidence:'):
        line_counter += 1
        splitter = line.split()
        values += float(splitter[1]) #after one experiment i found out that float value goes in index 1

print('Average spam confidence:', values / line_counter)

#I hope it helps you ;D
