from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
import csv
import os

def encrypt(plaintext, key, mode):
    cipher = AES.new(key, mode)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    
    if mode == AES.MODE_ECB:
        return ciphertext, None
    elif mode == AES.MODE_CTR:
        return ciphertext, cipher.nonce
    else:
        return ciphertext, cipher.iv

def decrypt(ciphertext, key, mode, iv_or_nonce):
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, mode)
    elif mode == AES.MODE_CTR:
        cipher = AES.new(key, mode, nonce=iv_or_nonce)
    else:
        cipher = AES.new(key, mode, iv=iv_or_nonce)
        
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

def main():
    csv_filename = "results.csv"
    with open(csv_filename, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Mode", "Encryption Time (s)", "Decryption Time (s)", "File Size (bytes)"])

    data = os.listdir('data')
    for filename in data:

        with open(f'data\\{filename}', 'r', encoding='utf-8') as file:
            plaintext = file.read()
            
        key = b'1234567890123456'
        modes = [AES.MODE_ECB, AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB, AES.MODE_CTR]
        
        mode_names = {
            AES.MODE_ECB: "ECB",
            AES.MODE_CBC: "CBC",
            AES.MODE_CFB: "CFB",
            AES.MODE_OFB: "OFB",
            AES.MODE_CTR: "CTR"
        }

        for mode in modes:
            mode_name = mode_names[mode]
            
            print(f"\nMode: {mode_name}")
            start_enc_time = time.time()
            
            ciphertext, iv_or_nonce = encrypt(plaintext, key, mode)
            end_enc_time = time.time()
            
            start_dec_time = time.time()
            
            decrypted_text = decrypt(ciphertext, key, mode, iv_or_nonce)
            end_dec_time = time.time()
            
            csv_filename = "results.csv"
            with open(csv_filename, mode='a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([mode_name, f"{end_enc_time - start_enc_time:.6f}", f"{end_dec_time - start_dec_time:.6f}", len(plaintext)])
                
            print(f"Encryption time: {end_enc_time - start_enc_time:.6f} seconds")
            print(f"Decryption time: {end_dec_time - start_dec_time:.6f} seconds")

if __name__ == "__main__":
    main()