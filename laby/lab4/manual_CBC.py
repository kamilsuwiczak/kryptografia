from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

def manual_cbc_encrypt(plaintext, key, iv):
    padded_data = pad(plaintext, AES.block_size)
    
    ecb_cipher = AES.new(key, AES.MODE_ECB)
    
    ciphertext = b''
    previous_block = iv
    
    for i in range(0, len(padded_data), AES.block_size):
        current_plaintext_block = padded_data[i:i+AES.block_size]
        
        xored_block = xor_bytes(current_plaintext_block, previous_block)
        
        encrypted_block = ecb_cipher.encrypt(xored_block)
    
        ciphertext += encrypted_block
        previous_block = encrypted_block
        
    return ciphertext

def manual_cbc_decrypt(ciphertext, key, iv):
    ecb_cipher = AES.new(key, AES.MODE_ECB)
    
    decrypted_padded_data = b''
    previous_block = iv
    
    for i in range(0, len(ciphertext), AES.block_size):
        current_ciphertext_block = ciphertext[i:i+AES.block_size]
        
        decrypted_block = ecb_cipher.decrypt(current_ciphertext_block)

        plaintext_block = xor_bytes(decrypted_block, previous_block)

        decrypted_padded_data += plaintext_block
        previous_block = current_ciphertext_block

    return unpad(decrypted_padded_data, AES.block_size)


if __name__ == "__main__":
    key = b'1234567890123456'
    iv = os.urandom(16)
    message = b"Wiadomosc do zaszyfrowania"
    
    print("Oryginalna wiadomość:", message)
    
    my_ciphertext = manual_cbc_encrypt(message, key, iv)
    print("Szyfrogram:", my_ciphertext.hex())
    
    my_decrypted = manual_cbc_decrypt(my_ciphertext, key, iv)
    print("Zdeszyfrowana wiadomość:", my_decrypted.decode('utf-8'))
    