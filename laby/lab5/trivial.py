import random

def trivial_split(s, n, k):
    
    shares = [random.randint(0, k - 1) for _ in range(n - 1)]
    
    s_n = (s - sum(shares)) % k
    shares.append(s_n)
    
    return shares

def trivial_reconstruct(shares, k):
    return sum(shares) % k
    

k = 1000
s = 420
n = 5

print(f"Parametry: sekret s={s}, przestrzeń k={k}, liczba udziałów n={n}")
udzialy = trivial_split(s, n, k)
print(f"Wygenerowane udziały: {udzialy}")

odtworzony_sekret = trivial_reconstruct(udzialy, k)
print(f"Odtworzony sekret: {odtworzony_sekret}")