cel = input("Enter celsius temperature: ")

try:
    cel = float(cel)
except:
    print("You didn't entered an allowed value!")
    quit()

faren = float( (cel * 1.8) + 32)


print(cel, "°C is equal to", faren, "°F")