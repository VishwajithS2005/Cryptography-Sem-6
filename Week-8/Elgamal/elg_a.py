import random
import socket

q = int(input("Enter the value of \'q\': "))
alpha = int(input("Enter a primitive root of \'q\': "))

X_a = random.randint(1, q-2)
Y_a = pow(alpha, X_a, q)
print(f"\nThe public key is: [{q}, {alpha}, {Y_a}].")

server = socket.socket()
server.bind(("127.0.0.1", 5678))
server.listen(1)
print("\nAlice has set up the server and is waiting for Bob.")
conn, addr = server.accept()
print(f"Bob has connected from {addr}.")
conn.send(str(q).encode().ljust(1024, b'\0'))
conn.send(str(alpha).encode().ljust(1024, b'\0'))
conn.send(str(Y_a).encode().ljust(1024, b'\0'))
print("The public key has been sent to Bob.")

C1 = int(conn.recv(1024).decode().rstrip('\0'))
C2 = int(conn.recv(1024).decode().rstrip('\0'))
print(f"Received ciphertext is: [{C1}, {C2}].")

K = pow(C1, X_a, q)
M = (C2 * pow(K, -1, q)) % q
print(f"\nThe message is: {M}.")

conn.close()
server.close()