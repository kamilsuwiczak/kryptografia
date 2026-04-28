import random
from Crypto.Util.number import getPrime
def shamir_split(s, n, t, p):
    
    print("ETAP PODZIAŁU")
    coeffs = [s] + [random.randint(1, p - 1) for _ in range(t - 1)]
    print(f"Współczynniki wielomianu (a_0 to nasz sekret): {coeffs}\n")
    
    shares = []
    for i in range(1, n + 1):
        val = sum(coeff * (i ** power) for power, coeff in enumerate(coeffs)) % p
        shares.append((i, val))
    
    print(f"Wygenerowane udziały (x, y): {shares}\n")
    return shares

def shamir_reconstruct(shares, p):
    print("ETAP ODTWARZANIA")
    secret = 0
    t = len(shares)
    print(f"Zebrane udziały do odtworzenia: {shares}\n")
    
    for i, (xi, yi) in enumerate(shares):
        num = 1
        den = 1
        for j, (xj, _) in enumerate(shares):
            if i != j:
                num = (num * (-xj)) % p
                den = (den * (xi - xj)) % p
        
        lagrange_coeff = (num * pow(den, -1, p)) % p
        term = (yi * lagrange_coeff) % p
        secret = (secret + term) % p
        print(f"Składnik wielomianu od udziału x={xi}: {term}")
        
    return secret

n = 6
t = 3
sekret = "SuperSekret"
s = int.from_bytes(sekret.encode('utf-8'), 'big')
p = getPrime(s.bit_length() + 1)

print(f"Parametry: całkowita liczba udziałów n={n}, wymagana t={t}, sekret s={s}, liczba pierwsza p={p}\n")

udzialy_shamir = shamir_split(s, n, t, p)

wybrane_udzialy = random.sample(udzialy_shamir, t)

odtworzony_shamir = shamir_reconstruct(wybrane_udzialy, p)
print(f"Odtworzony sekret: {odtworzony_shamir}")