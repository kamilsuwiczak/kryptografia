import hashlib
import time
import random
import string
import sys
import os


def generate_hash(input_string, algorithm):
    hash_object = hashlib.new(algorithm)
    hash_object.update(input_string.encode('utf-8'))
    print(f"{algorithm}: {hash_object.hexdigest()}")
    print(f"input length: {len(input_string)} hash length:{len(hash_object.hexdigest())}")

def get_hash_bin_from_bytes(byte_data, algorithm):
    h = hashlib.new(algorithm)
    h.update(byte_data)
    hex_digest = h.hexdigest()
    return bin(int(hex_digest, 16))[2:].zfill(len(hex_digest) * 4)

def find_collision_12bit(algorithm):
    seen_prefixes = {}
    attempts = 0
    while True:
        attempts += 1
        test_str = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        h = hashlib.new(algorithm)
        h.update(test_str.encode('utf-8'))
        prefix = h.hexdigest()[:3]
        
        if prefix in seen_prefixes:
            return test_str, seen_prefixes[prefix], prefix, attempts
        seen_prefixes[prefix] = test_str

def test_sac(algorithm, base_text="Lorem Ipsum is simply dummy"):
    original_bytes = base_text.encode('utf-8')
    original_bin = get_hash_bin_from_bytes(original_bytes, algorithm)
    bits_total = len(original_bin)
    
    total_diffs = 0
    tests_count = 0
    
    for i in range(len(original_bytes) * 8):
        modified_bytes = bytearray(original_bytes)
        modified_bytes[i // 8] ^= (1 << (i % 8))
        
        mod_hash_bin = get_hash_bin_from_bytes(modified_bytes, algorithm)
        
        diff = sum(1 for b1, b2 in zip(original_bin, mod_hash_bin) if b1 != b2)
        total_diffs += diff
        tests_count += 1
        
    avg_changed_bits = total_diffs / tests_count
    probability = avg_changed_bits / bits_total
    return avg_changed_bits, probability



def main():
    if not os.path.exists('data'):
        os.makedirs('data')
        
    data = os.listdir('data')
    print(f"Pliki w katalogu 'data': {data}")
    for filename in data:
        with open(os.path.join('data', filename), 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"\n========================================")
            print(f"--- Przetwarzanie pliku: {filename} ---")
            print(f"========================================")
            algorithms = ['md5', 'sha1', 'sha224','sha256', 'sha384', 'sha512']
            for algo in algorithms:
                print(f"\n--- {algo.upper()} | Plik: {filename} ---")
                start_time = time.perf_counter()
                generate_hash(content, algo)
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                print(f"Time taken: {elapsed_time:.6f} seconds\n")
                
                print(f"--- DODATKOWE BADANIA DLA {algo.upper()} ---")
                
                c_str1, c_str2, c_prefix, c_attempts = find_collision_12bit(algo)
                print(f"Kolizja 12-bit (prefix: {c_prefix}): znaleziono po {c_attempts} próbach.")
                print(f"Tekst 1: '{c_str1}' | Tekst 2: '{c_str2}'")
                
                sac_test_string = content[:64] if len(content) > 0 else "dummy text"
                sac_avg, sac_prob = test_sac(algo, sac_test_string)
                print(f"Test SAC: średnia zmiana bitów skrótu: {sac_avg:.2f}")
                print(f"Test SAC: prawdopodobieństwo zmiany bitu: {sac_prob:.4f}")

    
if __name__ == "__main__":
    main()