pt = input("Enter the text to be encoded: ")
d = int(input("Enter the depth: "))

ar = [[None for i in range(len(pt))] for j in range(d)]
row, col = 0,0
direction = 1

for i in pt:
    ar[row][col] = i
    col += 1
    row += direction
    if row == 0 or row == d-1:
        direction *= -1
print(ar)
ct = ""
for i in ar:
    for j in i:
        if j != None:
            ct += j

print("The Cipher Text is: " +  ct)

row, col = 0,0
direction = 1
ar1 = [[None for i in range(len(ct))] for j in range(d)]
for i in ct:
    ar1[row][col] = '*'
    col += 1
    row += direction
    if row == 0 or row == d-1:
        direction *= -1
index = 0
for i in range(d):
    for j in range(len(ct)):
        if index < len(ct) and ar1[i][j] == '*':
            ar1[i][j] = ct[index]
            index += 1
print(ar1)
row, col = 0,0
direction = 1
pt1 = ""
while len(pt1) < len(ct):
    pt1 += ar[row][col]
    col += 1
    row += direction
    if row == 0 or row == d-1:
        direction *= -1
print("The plaintext is: " + pt)