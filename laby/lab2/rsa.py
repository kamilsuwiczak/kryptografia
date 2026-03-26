from Crypto.Util.number import getPrime
from math import gcd

def generate_keys(bits=1024):
    p = getPrime(bits)
    while p < 999:
        p = getPrime(bits)
    
    q = getPrime(bits)

    while q < 999 or q == p:
        q = getPrime(bits)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    e = getPrime(bits)
    
    while gcd(e,phi) != 1:
        e = getPrime(bits)
    
    d = pow(e, -1, phi)
    public_key = (e,n)
    private_key = (d,n)
    return public_key, private_key

def encrypt(message, public_key):
    message = int.from_bytes(message.encode(), 'big')
    e, n = public_key
    return pow(message, e, n)

def decrypt(ciphertext, private_key):
    d, n = private_key
    m = pow(ciphertext, d, n)
    byte_length = (m.bit_length() + 7) // 8
    return m.to_bytes(byte_length, 'big').decode()


def main():
    public_key, private_key = generate_keys()
    print(f"Public Key: {public_key}\n")
    print(f"Private Key: {private_key}\n")

    message = "consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"
    # print(f"Length of original message in bits: {message.encode().__len__() * 8}\n")

    ciphertext = encrypt(message, public_key)
    decrypted_message = decrypt(ciphertext, private_key)

    print(f"Original Message: {message}\n")
    print(f"Ciphertext: {ciphertext}\n")
    print(f"Decrypted Message: {decrypted_message}\n")

if __name__ == "__main__":
    main()
    