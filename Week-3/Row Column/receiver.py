import socket
import pickle

server = socket.socket()
server.bind(('127.0.0.1', 5096))
server.listen(1)
print("Row Column Cipher Receiver initialized and listening for sender.")

conn, addr = server.accept()
print(f"Connection established with sender at {addr}.")
ct = conn.recv(1024).decode().rstrip('\0')
print(f"The Cipher Text is: {ct}.")
key = pickle.loads(conn.recv(1024).rstrip(b'\0'))
pt_len = int(conn.recv(1024).decode().rstrip('\0'))
print(f"The permutation is: {key}")

conn.close()
server.close()

d = dict()
gap = len(ct)//len(key)
for i in range(1, len(key)+1):
    d[i] = ct[(i-1)*gap : i*gap]

mat = [[None for i in range(len(key))] for j in range(gap)]
for i in range(len(key)):
    block = d[key[i]]
    for j in range(gap):
        mat[j][i] = block[j]
print("\nThe intermediate matrix is:")
pt = ""
for i in mat:
    for j in i:
        print(j, end=" ")
        pt += j
    print()
print()

print(f"The Plain Text with padding is: \"{pt}\".")
pt = pt[:pt_len]
print(f"The Plain Text without padding is: \"{pt}\".")