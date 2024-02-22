def computepay(hours,rate):
    #print("In computepay", hours, rate)
    if hours > 40:
        regular = hours * rate
        overtime = (hours - 40) * (rate * 0.5)
        pay = regular + overtime
    else:
        pay = hours * rate
    #print("Returning", pay)
    return pay

hours = input("Enter Hours: ")
rate = input("Enter Rate: ")
hours = float(hours)
rate = float(rate)

pay = computepay(hours,rate)




print ("Pay", pay)
