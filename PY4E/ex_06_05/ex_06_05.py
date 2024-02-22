str = 'X-DSPAM-Confidence:0.8475'
position = str.find(":") #Finding where the number starts
number = str[position + 1:] #Saving the number in a variable

print(float(number))