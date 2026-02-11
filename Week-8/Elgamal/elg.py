import random

q = int(input("Enter the value of \'q\': "))
alpha = int(input("Enter a primitive root of \'q\': "))

#Key generation by Alice
X_a = random.randint(1, q-2)
Y_a = pow(alpha, X_a, q)
print(f"\nThe public key is: [{q}, {alpha}, {Y_a}].")

#encryption by bob
M = int(input("\nEnter a plaintext less than the value of q: "))
k = random.randint(1, q-1)
K = pow(Y_a, k, q)
C1 = pow(alpha, k, q)
C2 = (K * M) % q
print(f"The ciphertext is: [{C1}, {C2}].")

#decryption by alice
K = pow(C1, X_a, q)
M = (C2 * pow(K, -1, q)) % q
print(f"\nThe message is: {M}.")