import socket

def create_diagram(pt):
    diagram = []
    i = 0
    while i < len(pt):
        a = pt[i]
        if i + 1 < len(pt):
            b = pt[i + 1]
            if a == b:
                diagram.append(a + 'x')
                i += 1
            else:
                diagram.append(a + b)
                i += 2
        else:
            diagram.append(a + 'x')
            i += 1
    return diagram

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

def get_cipher(diagram, key_matrix):
    cipher_text = ""
    for pair in diagram:
        row1, col1, row2, col2 = -1, -1, -1, -1
        for r in range(5):
            for c in range(5):
                if key_matrix[r][c] == pair[0]:
                    row1, col1 = r, c
                if key_matrix[r][c] == pair[1]:
                    row2, col2 = r, c
        if row1 == row2:
            cipher_text += key_matrix[row1][(col1 + 1) % 5]
            cipher_text += key_matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            cipher_text += key_matrix[(row1 + 1) % 5][col1]
            cipher_text += key_matrix[(row2 + 1) % 5][col2]
        else:
            cipher_text += key_matrix[row1][col2]
            cipher_text += key_matrix[row2][col1]
    return cipher_text

print("Playfair Cipher Sender initialized.")
pt = input("Enter the plaintext: ").lower()
if(len(pt) == 0):
    print("No plaintext provided. Exiting.")
    exit()
key = input("Enter the key: ").lower()
if(len(key) == 0):
    print("No key provided. Exiting.")
    exit()

diagram = create_diagram(pt)
diagram_text = ''.join(diagram)
print("Diagram created:", diagram_text)
key_matrix = create_key_matrix(key)
print("Key matrix created:")
for row in key_matrix:
    print(row)
cipher_text = get_cipher(diagram, key_matrix)
print("Ciphertext generated:", cipher_text)

s = socket.socket()
s.connect(('127.0.0.1', 5067))
s.send(cipher_text.encode().ljust(1024, b'\0'))
s.send(key.encode().ljust(1024, b'\0'))
print("Ciphertext and key sent to the receiver.")
s.close()