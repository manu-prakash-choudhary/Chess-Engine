strng = "{"
ord = 97
for i in range(0,8):
    strng += '"' + chr(ord)+'"' + ': ' + str(i) + ", "
    ord += 1
strng += '}'
print(strng)
