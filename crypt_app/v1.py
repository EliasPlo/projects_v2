import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# AES käyttää 16 tavun (128-bit) blokkikokoja
BLOCK_SIZE = 16

def pad(data):
    """Lisää täyte, jotta data on BLOCK_SIZE:n monikerta."""
    padding = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([padding] * padding)

def unpad(data):
    """Poistaa täytteen."""
    padding = data[-1]
    return data[:-padding]

def encrypt_file(file_path, key):
    """Salaa tiedoston."""
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    
    # Luo salausobjekti
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    
    # Salaa data
    ciphertext = cipher.encrypt(pad(plaintext))
    
    # Kirjoita salattu tiedosto
    with open(file_path + '.enc', 'wb') as f:
        f.write(iv + ciphertext)

    print(f"File '{file_path}' has been encrypted to '{file_path}.enc'.")

def decrypt_file(file_path, key):
    """Puraa salaus tiedostosta."""
    with open(file_path, 'rb') as f:
        data = f.read()
    
    # Lue IV ja salattu sisältö
    iv = data[:BLOCK_SIZE]
    ciphertext = data[BLOCK_SIZE:]
    
    # Luo purkuobjekti
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext))
    
    # Kirjoita purettu tiedosto
    original_file = file_path.replace('.enc', '.dec')
    with open(original_file, 'wb') as f:
        f.write(plaintext)

    print(f"File '{file_path}' has been decrypted to '{original_file}'.")

# Testaaminen
if __name__ == "__main__":
    # Luo 32 tavun salausavain
    secret_key = get_random_bytes(32)
    print(f"Secret Key (keep this safe!): {secret_key.hex()}")

    # Salaa tiedosto
    encrypt_file('example.txt', secret_key)
    
    # Puraa tiedosto
    decrypt_file('example.txt.enc', secret_key)
