import socket
import random
import json

sa = socket.socket()
print("Attacker sends Y_D1 to Alice pretending to be Bob")
sa.connect(("127.0.0.1", 10000))
payload1 = json.loads(sa.recv(1024).decode('utf-8'))

P = payload1["P"]
G = payload1["G"]
Y_A = payload1["Y_A"]
X_D1 = random.randint(2, P - 2)
X_D2 = random.randint(2, P - 2)
Y_D1 = pow(G, X_D1, P)
Y_D2 = pow(G, X_D2, P)
sa.sendall(json.dumps({"Y_D1": Y_D1}).encode('utf-8'))

sb = socket.socket()
print("Attacker sends Y_D2 to Bob pretending to be Alice")
sb.connect(("127.0.0.1", 9000))

payload2 = json.dumps({
"P": P,
"G": G,
"Y_D2": Y_D2
})
sb.sendall(payload2.encode('utf-8'))

payload3 = json.loads(sb.recv(1024).decode('utf-8'))
KAA = pow(int(payload1["Y_A"]), X_D1, P)
KAB = pow(int(payload3["Y_B"]), X_D2, P)

print(f"The prime number is {P}")
print(f"The primitive root of the prime number is {G}")
print(f"Randomly generated private key for Alice is {X_D1}")
print(f"Randomly generated private key for Alice is {X_D2}")
print(f"Computed public key for Alice is {Y_D1}")
print(f"Computed public key for Bob is {Y_D2}")
print(f"Common key between Attacker and Alice that Attacker has is {KAA}")
print(f"Common key between Attacker and Bob that Attacker has is {KAB}")

sa.close()
sb.close()