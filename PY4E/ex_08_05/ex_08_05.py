try:
    file = open(input("Enter a file name: "))
except:
    print("Invalid file name.")

user =[]

for line in file:
    if line.startswith("From: "):
        line.strip()
        line.split()
        user.append(line[2])
        print(user)
