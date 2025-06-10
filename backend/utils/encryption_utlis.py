# this file provides :
# encrypt_file()--> encrypts a file and store encrypted version
# decrypt_file()--> decrypts encrypted file --> returns decrypted version for download.

# fernet is a class in cryptography  provide symmetric encryption i.e same key is used to encrypt & decrypt
# Fernet provides simple and secure symmetric encryption with built-in integrity checking.
from cryptography.fernet import Fernet
import os
import shutil # used to copy files

from dotenv import load_dotenv
load_dotenv()
FERNET_KEY = os.getenv("FERNET_KEY")

# Setup Fernet
fernet = Fernet(FERNET_KEY) # creating fernet object using secret key to encrypt and decrypt data.

# Encrypt file → returns encrypted file path
def encrypt_file(file_path: str) -> str:
    with open(file_path, "rb") as file: # open file in binary mode--> "rb"--> read all its data
        original_data = file.read()

    encrypted_data = fernet.encrypt(original_data)

    # Save encrypted file
    encrypted_file_path = file_path + ".enc" # define output path and add .enc at suffix.
    # write encrypted data into .enc file
    with open(encrypted_file_path, "wb") as file: 
        file.write(encrypted_data)

    return encrypted_file_path

# Decrypt file → returns decrypted file path
def decrypt_file(encrypted_file_path: str) -> str:
    with open(encrypted_file_path, "rb") as file: #  Read the encrypted data.
        encrypted_data = file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    # Save decrypted file temporarily → for download
    decrypted_file_path = encrypted_file_path.replace(".enc", ".dec")
    with open(decrypted_file_path, "wb") as file: # write decrypted data to .dec file
        file.write(decrypted_data)

    return decrypted_file_path

# Encrypt bytes → new function for simple Upload API
def encrypt_bytes(data: bytes, output_path: str) -> str:
    encrypted_data = fernet.encrypt(data)
    with open(output_path, "wb") as file:
        file.write(encrypted_data)
    return output_path


      