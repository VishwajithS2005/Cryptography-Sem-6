import socket
import random
import sympy
import json

P = sympy.randprime(10000, 50000)
G = sympy.primitive_root(P)
X_A = random.randint(2, P - 2)
Y_A = pow(G, X_A, P)

server = socket.socket()
server.bind(("127.0.0.1", 10000))
server.listen(1)
print("Waiting for Bob (but will recieve from attacker instead)...")
conn, addr = server.accept()
payload1 = json.dumps({
"P": P,
"G": G,
"Y_A": Y_A
})
conn.sendall(payload1.encode('utf-8'))

payload2 = json.loads(conn.recv(1024).decode('utf-8'))
KA = pow(int(payload2["Y_D1"]), X_A, P)

print(f"The prime number is {P}")
print(f"The primitive root of the prime number is {G}")
print(f"Randomly generated private key is {X_A}")
print(f"Computed public key is {Y_A}")
print(f"Public key from attacker is {payload2["Y_D1"]}")
print(f"Common key between Attacker and Alice that Alice has is {KA}")

conn.close()