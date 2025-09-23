import os

from cryptography.fernet import Fernet

DATA_FILE = "wallets.csv"
ENCRYPTED_FILE = "wallets.csv.enc"
KEY_FILE = "secret.key"


def generate_key(file_path: str = KEY_FILE):
    key = Fernet.generate_key()
    with open(file_path, "wb") as file:
        file.write(key)

    return key


def load_key(file_path: str = KEY_FILE):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Key file {file_path} not found.")

    with open(file_path, "rb") as file:
        return file.read()


def secure_delete(file_path: str, passes: int = 3):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")

    lenght = os.path.getsize(file_path)
    with open(file_path, "ba+", buffering=0) as delfile:
        for _ in range(passes):
            delfile.seek(0)
            delfile.write(os.urandom(lenght))

    os.remove(file_path)


def encrypt_file(source_path: str, dist_path: str):
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"File {source_path} not found.")

    key = generate_key()
    fernet = Fernet(key)

    with open(source_path, "rb") as file_in:
        original = file_in.read()

    encrypted = fernet.encrypt(original)

    with open(dist_path, "wb") as file_out:
        file_out.write(encrypted)

    secure_delete(source_path)


def decrypt_file(source_path: str, dist_path: str):
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"File {source_path} not found.")

    key = load_key()
    fernet = Fernet(key)

    with open(source_path, "rb") as file_in:
        encrypted = file_in.read()

    decrypted = fernet.decrypt(encrypted)

    with open(dist_path, "wb") as file_out:
        file_out.write(decrypted)


if __name__ == "__main__":
    action = input("What to do? [e]ncrypt or [d]ecrypt: ").strip().lower()

    if action == "e":
        encrypt_file(DATA_FILE, ENCRYPTED_FILE)
    elif action == "d":
        decrypt_file(ENCRYPTED_FILE, DATA_FILE)
    else:
        print('[-] Invalid command. Use "e" for encryption or "d" for decryption')
