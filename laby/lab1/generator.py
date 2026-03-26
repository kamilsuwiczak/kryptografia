
import math
from Crypto.Util.number import getPrime, getRandomRange

def gen_blum_prime(num_of_bits):
    while True:
        candidate = getPrime(num_of_bits)
        if(candidate % 4 == 3):
            return candidate

def gen_blum_number(num_of_bits):
    p = gen_blum_prime(num_of_bits)
    q = gen_blum_prime(num_of_bits)
    if p <1000:
        p = gen_blum_prime(num_of_bits)
    if q <1000:
        q = gen_blum_prime(num_of_bits)
    while p==q:
        q = gen_blum_prime(num_of_bits)
    return p*q

def gen_bbs_series(stream_length,num_of_bits):
    N = gen_blum_number(num_of_bits)
    while True:
        x0 = getRandomRange(2, N)
        if math.gcd(x0, N) == 1:
            break
    x_i = pow(x0, 2, N)
    output = []
    for _ in range(stream_length):
        x_i = pow(x_i, 2, N)
        lsb = x_i & 1
        output.append(lsb)
    return output


def main():
    print("Generating Blum Blum Shub series...")
    series = gen_bbs_series(20_000, 512)
    with open("output.txt", "w") as f:
        for i in series:
            f.write(f"{i}\n")
    print(f"Generated series: {series}, length: {len(series)}")
    return series

if __name__ == "__main__":
    main()
