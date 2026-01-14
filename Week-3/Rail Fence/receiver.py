import socket

server = socket.socket()
server.bind(('127.0.0.1', 12345))
server.listen(1)
print("Rail Fence Cipher Receiver initialized and listening for sender.")

conn, addr = server.accept()
print(f"Connection established with sender at {addr}.")
ct = conn.recv(1024).decode().rstrip('\0')
d = int(conn.recv(1024).decode().rstrip('\0'))

print(f"Received Cipher Text is: {ct}.")
print(f"Received depth is: {d}.")

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

print("The intermediate matrix is:")
for i in ar1:
    for j in i:
        if j == None:
            print("-", end=" ")
        else:
            print(j, end=" ")
    print()
print()

row, col = 0,0
direction = 1
pt1 = ""
while len(pt1) < len(ct):
    pt1 += ar1[row][col]
    col += 1
    row += direction
    if row == 0 or row == d-1:
        direction *= -1
print("The plaintext is: " + pt1)

conn.close()
server.close()