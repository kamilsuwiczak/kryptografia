from Crypto.Util.number import getPrime, isPrime
import random

def generate_dh_parameters(bits=512):

    found = False
    while not found:
        q = getPrime(bits - 1)
        n = 2 * q + 1
        if isPrime(n):
            found = True
            
    print(f"Znaleziono n: {n}")
    
    for g in range(2, n):
        if pow(g, 2, n) != 1 and pow(g, q, n) != 1:
            return n, g

def diffie_hellman():
    n, g = generate_dh_parameters(64)
    print(f"Publiczne parametry: n={n}, g={g}\n")

    x = random.randint(1, n-1)
    X = pow(g, x, n)
    print(f"Alicja: mój tajny x = {x}, wysyłam do Boba X = {X}")

    y = random.randint(1, n-1)
    Y = pow(g, y, n)
    print(f"Bob: mój tajny y = {y}, wysyłam do Alicji Y = {Y}\n")

    k_alicja = pow(Y, x, n)
    
    k_bob = pow(X, y, n)

    print(f"Klucz obliczony przez Alicję: {k_alicja}")
    print(f"Klucz obliczony przez Boba: {k_bob}")

    if k_alicja == k_bob:
        print("\nObie strony mają ten sam klucz sesji")

if __name__ == "__main__":
    diffie_hellman() 