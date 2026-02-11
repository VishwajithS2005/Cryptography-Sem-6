import socket
import random

s = socket.socket()
s.connect(("127.0.0.1", 5678))
print("Bob has been initialized and connected to Alice.")
q = int(s.recv(1024).decode().rstrip('\0'))
alpha = int(s.recv(1024).decode().rstrip('\0'))
Y_a = int(s.recv(1024).decode().rstrip('\0'))
print(f"\nReceived public key is: [{q}, {alpha}, {Y_a}].")

M = int(input("\nEnter a plaintext less than the value of q: "))
k = random.randint(1, q-1)
K = pow(Y_a, k, q)
C1 = pow(alpha, k, q)
C2 = (K * M) % q
print(f"The ciphertext is: [{C1}, {C2}].")

s.send(str(C1).encode().ljust(1024, b'\0'))
s.send(str(C2).encode().ljust(1024, b'\0'))

print("The ciphertext has been sent to Alice.")
s.close()