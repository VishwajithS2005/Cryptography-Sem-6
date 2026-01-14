import pickle
import socket

print("Row Column Cipher Sender Initialized.")
pt = input("Enter the plaintext: ")
pt_len = len(pt)
key = input("Enter the permutation: ").split(" ")
key = [int(i) for i in key]
key_data = pickle.dumps(key)


if max(key) != len(key) or min(key) != 1:
    print("The given permutation is invalid.")
    exit(1)

if len(pt) % len(key) != 0:
    pad = len(key) - (pt_len % len(key))
    pt += '*'*pad

mat = [[None for i in range(len(key))] for j in range(len(pt)//len(key))]
index = 0
for i in range(len(pt)//len(key)):
    for j in range(len(key)):
        if index < len(pt):
            mat[i][j] = pt[index]
            index += 1
print("\nThe intermediate matrix is:")
for i in mat:
    for j in i:
        print(j, end=" ")
    print()
print()

d = dict()
for i in range(len(key)):
    d[key[i]] = ""
    for j in range(len(pt)//len(key)):
        d[key[i]] += mat[j][i]

ct = ""
for i in sorted(d.keys()):
    ct += d[i]
print(f"The Cipher Text is: \"{ct}\".")

s = socket.socket()
s.connect(('127.0.0.1', 5096))
s.send(ct.encode().ljust(1024, b'\0'))
s.send(key_data.ljust(1024, b'\0'))
s.send(str(pt_len).encode().ljust(1024, b'\0'))
print("The Ciphertext, permutation and the original plain text length have been sent successfully.")
s.close()