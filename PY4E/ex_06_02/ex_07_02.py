fname = input("Enter file name: ")


try:
    fname = open(fname)
except:
    print("Invalid file name!")
    quit()

count = 0
num = 0

for line in fname:
    if line.startswith("X-DSPAM-Confidence:"):
        count = count + 1
        fline = line.find(":")
        fnum  = line[fline + 1:]
        fnum  = fnum.strip()
        print(fnum)

print(count)
total = float(fnum) / count

print("Average spam confidence:", total)
