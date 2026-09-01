import os
import json
import secrets
import string
import glob
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"
VAULT_DIR = "vaults"

def initialize_system():
    if not os.path.exists(VAULT_DIR):
        os.makedirs(VAULT_DIR)
        
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError("Clave maestra no encontrada.")
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def generate_password(name, lock_time_minutes):
    vault_path = os.path.join(VAULT_DIR, f"{name}.vault")
    if os.path.exists(vault_path):
        raise FileExistsError(f"Ya existe una bóveda con el nombre '{name}'.")

    chars = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(chars) for _ in range(32))
    
    data = {
        "password": password,
        "lock_time_minutes": lock_time_minutes
    }
    json_data = json.dumps(data)
    
    key = load_key()
    f = Fernet(key)
    
    encrypted = f.encrypt(json_data.encode('utf-8'))
    
    with open(vault_path, "wb") as vault_file:
        vault_file.write(encrypted)
        
    return password

def list_vaults():
    vaults = glob.glob(os.path.join(VAULT_DIR, "*.vault"))
    return [os.path.splitext(os.path.basename(v))[0] for v in vaults]

def load_vault_info(name):
    """Carga y desencripta el archivo para leer el tiempo de bloqueo (sin revelar al usuario todavía, uso interno)."""
    vault_path = os.path.join(VAULT_DIR, f"{name}.vault")
    if not os.path.exists(vault_path):
        raise FileNotFoundError("Bóveda no encontrada.")
        
    key = load_key()
    f = Fernet(key)
    
    with open(vault_path, "rb") as vault_file:
        encrypted = vault_file.read()
        
    try:
        decrypted = f.decrypt(encrypted).decode('utf-8')
        data = json.loads(decrypted)
        return data
    except Exception:
        raise ValueError("Error al desencriptar la bóveda.")
