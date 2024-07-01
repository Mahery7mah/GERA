# utils.py
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode, urlsafe_b64decode

def generate_key():
    return Fernet.generate_key()

def encrypt_id(id_to_encrypt, key):
    cipher_suite = Fernet(key)
    encrypted_id = cipher_suite.encrypt(str(id_to_encrypt).encode())
    return urlsafe_b64encode(encrypted_id).decode()

def decrypt_id(encrypted_id, key):
    encrypted_id += '=' * (len(encrypted_id) % 4)  
    encrypted_id_bytes = urlsafe_b64decode(encrypted_id)
    cipher_suite = Fernet(key)
    
    try:
        decrypted_id = cipher_suite.decrypt(encrypted_id_bytes).decode()
        return int(decrypted_id)
    except Exception as e:
        print(f"Error in decrypt_id: {e}")
        return None