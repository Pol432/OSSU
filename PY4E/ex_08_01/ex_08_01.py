def chop(x):
    del(x[0])
    del(x[-1])
    return(None)

def middle(x):
    del(x[0])
    del(x[-1])
    return(x)

y = ["1","2","3","4","5","6"]
x = ["1","2","3","4","5","6"]

print(chop(y))
print(middle(x))
