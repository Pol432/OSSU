import urllib.request

web = urllib.request.urlopen("http://data.pr4e.org/romeo.txt")
for line in web:
    print(line.decode().strip())
