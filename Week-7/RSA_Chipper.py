import random

def nBitRandom(n):
    return random.randrange(2**(n-1) + 1, 2**n - 1)

first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

def getLowLevelPrime(n):
    while True:
        pc = nBitRandom(n)
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor**2 <= pc:
                break
        else:
            return pc

def isMillerRabinPassed(mrc):
    maxDivisionsByTwo = 0
    ec = mrc - 1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert 2**maxDivisionsByTwo * ec == mrc - 1

    def trialComposite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2**i * ec, mrc) == mrc - 1:
                return False
        return True

    numberOfRabinTrials = 20
    for _ in range(numberOfRabinTrials):
        round_tester = random.randrange(2, mrc)
        if trialComposite(round_tester):
            return False
    return True

def generateLargePrime(n=1024):
    while True:
        prime_candidate = getLowLevelPrime(n)
        if isMillerRabinPassed(prime_candidate):
            return prime_candidate

P = generateLargePrime(1024)
Q = generateLargePrime(1024)
n = P * Q
phi_n = (P - 1) * (Q - 1)
e = 65537
d = pow(e, -1, phi_n)
M = int(input("Enter the message (a number): "))
C = pow(M, e, n)
D = pow(C, d, n)

print(f"\nValue of p is: {P}.")
print(f"Value of q is: {Q}.")
print(f"Value of n is: {n}.")
print(f"Value of phi(n) is: {phi_n}.")
print(f"Value of e is: {e}.")
print(f"Value of d is: {d}.")
print(f"Encrypted text is: {C}.")
print(f"Decrypted text is: {D}.")