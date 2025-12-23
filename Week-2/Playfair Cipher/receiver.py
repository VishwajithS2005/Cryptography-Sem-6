import socket

def create_key_matrix(key):
    key = key.replace("j", "i")
    key_matrix = []
    used_chars = set()
    row = 0
    col = 0
    temp = []
    for char in key:
        if char not in used_chars and char.isalpha():
            used_chars.add(char)
            temp.append(char)
            col += 1
            if col == 5:
                key_matrix.append(temp)
                temp = []
                row += 1
                col = 0
    for i in range(ord('a'), ord('z') + 1):
        char = chr(i)
        if char == 'j':
            continue
        if char not in used_chars:
            used_chars.add(char)
            temp.append(char)
            col += 1
            if col == 5:
                key_matrix.append(temp)
                temp = []
                row += 1
                col = 0
    return key_matrix

def get_plain_text(cipher, key_matrix):
    plain_text = ""
    for i in range(0, len(cipher), 2):
        pair = cipher[i:i+2]
        row1, col1, row2, col2 = -1, -1, -1, -1
        for r in range(5):
            for c in range(5):
                if key_matrix[r][c] == pair[0]:
                    row1, col1 = r, c
                if key_matrix[r][c] == pair[1]:
                    row2, col2 = r, c
        if row1 == row2:
            plain_text += key_matrix[row1][(col1 - 1) % 5]
            plain_text += key_matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plain_text += key_matrix[(row1 - 1) % 5][col1]
            plain_text += key_matrix[(row2 - 1) % 5][col2]
        else:
            plain_text += key_matrix[row1][col2]
            plain_text += key_matrix[row2][col1]
    return plain_text

server = socket.socket()
server.bind(('127.0.0.1', 5067))
server.listen(1)
print("Playfair Cipher Receiver initialized and listening for sender.")
conn, addr = server.accept()
print(f"Connection established with {addr}.")

cipher = conn.recv(1024).decode().rstrip('\0')
key = conn.recv(1024).decode().rstrip('\0')
print("Ciphertext received:", cipher)
print("Key received:", key)
key_matrix = create_key_matrix(key)
print("Plain text reconstructed:", get_plain_text(cipher, key_matrix))

conn.close()
server.close()