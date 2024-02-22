hours = input("Enter Hours: ")
rate = input("Enter Rate: ")
hours = float(hours)
rate = float(rate)

#print(fh,fr)

if hours > 40:
    #print("Overtime")
    regular = hours * rate
    overtime = (hours - 40) * (rate * 0.5)
    #print(regular, overtime)
    pay = regular + overtime
else:
    #print("Regular")
    pay = hours * rate


print ("Pay:", pay)
