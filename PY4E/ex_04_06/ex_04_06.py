
def computepay(hours,rate):
    if hours > 40:
        ephours = hours - 40
        pay = (hours  * rate) + (ephours * 0.5 * rate)
        return pay
    else:
        pay = hours * rate
        return pay
try:
    hours = float(input("Enter Hours: "))
    rate = float(input("Enter Rate: "))
except:
    print("Invalid input!")
    quit()

payment = computepay(hours,rate)
print(payment)

#try:
    #hours = float(input("Enter Hours: "))
    #rate = float(input("Enter Rate: "))
#except:
    #print("Invalid Input")
    #quit()

#print ("Pay:", pay)
