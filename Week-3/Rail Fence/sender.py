import socket

print("Rail Fence Cipher Sender Initialized.")
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

print("\nThe intermediate matrix is:")
for i in ar:
    for j in i:
        if j == None:
            print("-", end=" ")
        else:
            print(j, end=" ")
    print()
print()

ct = ""
for i in ar:
    for j in i:
        if j != None:
            ct += j

print("The Cipher Text is: " +  ct)

s = socket.socket()
s.connect(('127.0.0.1', 12345))
s.send(ct.encode().ljust(1024, b'\0'))
s.send(str(d).encode().ljust(1024, b'\0'))
print("Cipher text and the depth are sent successfully.")
s.close()