import socket
import random
import json

server = socket.socket()
server.bind(("127.0.0.1", 9000))
server.listen(1)
print("Waiting for Alice (but will recieve from attacker instead)...")
conn, addr = server.accept()
payload = json.loads(conn.recv(1024).decode('utf-8'))

P = payload["P"]
G = payload["G"]
X_B = random.randint(2, P - 2)
Y_B = pow(G, X_B, P)
KB = pow(int(payload["Y_D2"]), X_B, P)

print(f"The prime number is {P}")
print(f"The primitive root of the prime number is {G}")
print(f"Randomly generated private key is {X_B}")
print(f"Computed public key is {Y_B}")
print(f"Public key from attacker is {payload["Y_D2"]}")
print(f"Common key between Attacker and Bob that Bob has is {KB}")

conn.sendall(json.dumps({"Y_B": Y_B}).encode('utf-8'))
conn.close()
server.close()