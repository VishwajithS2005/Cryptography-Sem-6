import socket
import numpy as np

def create_key_matrix(key_text, n):
    key_matrix = []
    index = 0
    for i in range(n):
        row = []
        for j in range(n):
            row.append(ord(key_text[index]) - ord('a'))
            index += 1
        key_matrix.append(row)
    return np.matrix(key_matrix, dtype=int)

def create_ct_matrix(ct, n):
    ct_matrix = []
    for i in range(0, len(ct), n):
        row = [ord(char) - ord('a') for char in ct[i:i+n]]
        ct_matrix.append(row)
    return np.matrix(ct_matrix, dtype=int)

def get_key_matrix_adjugate(key_matrix):
    n = key_matrix.shape[0]
    adjugate = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            minor = np.delete(np.delete(key_matrix, i, axis=0), j, axis=1)
            cofactor = int(round(np.linalg.det(minor))) * ((-1) ** (i + j))
            adjugate[j][i] = cofactor % 26
    return np.asmatrix(adjugate)

def get_plain_text(pt_matrix):
    pt = ''
    for row in pt_matrix:
        for num in row.tolist()[0]:
            pt += chr(num + ord('a'))
    return pt

server = socket.socket()
server.bind(('127.0.0.1', 5069))
server.listen(1)
print("Hill Cipher Receiver initialized and listening for sender.")

conn, addr = server.accept()
print(f"Connection established with sender at {addr}.")
ct = conn.recv(1024).decode().rstrip('\0')
n = int(conn.recv(1024).decode().rstrip('\0'))
key_text = conn.recv(1024).decode().rstrip('\0')

print(f"Received Ciphertext: {ct}")
print(f"Received Key Size: {n}")
print(f"Received Key Text: {key_text}")

key_matrix = create_key_matrix(key_text, n)
print("Key Matrix:")
for row in key_matrix:
    print(row)

ct_matrix = create_ct_matrix(ct, n)
print("Ciphertext Matrix:")
for row in ct_matrix:
    print(row)

det = int(round(np.linalg.det(key_matrix))) % 26
det_inverse = pow(det, -1, 26)
print(f"Determinant: {det}")
print(f"Determinant Inverse: {det_inverse}")

key_matrix_inverse = (det_inverse * get_key_matrix_adjugate(key_matrix)) % 26
print("Inverse Key Matrix:")
for row in key_matrix_inverse:
    print(row)

pt_matrix = (ct_matrix @ key_matrix_inverse) % 26
print("Plaintext Matrix:")
for row in pt_matrix:
    print(row)

pt = get_plain_text(pt_matrix)
print(f"Decrypted Plaintext: {pt}")

conn.close()
server.close()