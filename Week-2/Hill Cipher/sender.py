import socket
import numpy as np

def create_key_matrix(key_char_matrix):
    key_matrix = [[ord(char) - ord('a') for char in row] for row in key_char_matrix]
    return np.matrix(key_matrix, dtype=int)

def create_pt_matrix(pt, n):
    pt_matrix = []
    for i in range(0, len(pt), n):
        row = [ord(char) - ord('a') for char in pt[i:i+n]]
        pt_matrix.append(row)
    return np.matrix(pt_matrix, dtype=int)

def get_cipher_text(ct_matrix):
    ct = ''
    for row in ct_matrix:
        for num in row.tolist()[0]:
            ct += chr(num + ord('a'))
    return ct

def get_key_text(key_char_matrix):
    key = ''
    for row in key_char_matrix:
        for char in row:
            key += char
    return key

print("Hill Cipher Sender initialized.")
n = int(input("Enter the size of the key matrix (n x n): "))
pt = input(f"Enter the plaintext: ").lower()
key_char_matrix = [list(input(f"Enter row {i+1} of the key matrix (space-separated integers and length must be {n}): ").lower()) for i in range(n)]
key_matrix = create_key_matrix(key_char_matrix)
key_text = get_key_text(key_char_matrix)
print("Key Matrix:")
for row in key_matrix:
    print(row)
print(f"Key Text: {key_text}")

pt_matrix = create_pt_matrix(pt, n)
print("Plaintext Matrix:")
for row in pt_matrix:
    print(row)

ct_matrix = (pt_matrix @ key_matrix) % 26
print("Ciphertext Matrix:")
for row in ct_matrix:
    print(row)

ct = get_cipher_text(ct_matrix)
print(f"Ciphertext: {ct}")

s = socket.socket()
s.connect(('127.0.0.1', 5069))
s.send(ct.encode().ljust(1024, b'\0'))
s.send(str(n).encode().ljust(1024, b'\0'))
s.send(key_text.encode().ljust(1024, b'\0'))
print("Ciphertext, key size, and key text sent to receiver.")
s.close()