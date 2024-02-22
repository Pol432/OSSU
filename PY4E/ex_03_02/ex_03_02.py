
try:
    hours = float(input("Enter Hours: "))
    rate = float(input("Enter Rate: "))
except:
    print("Invalid Input")
    quit()


if hours > 40:
    ephours = hours - 40
    pay = ((hours - ephours) * rate) + (ephours * 1.5 * rate)
else:
    pay = hours * rate


print ("Pay:", pay)
