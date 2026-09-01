import os
import sys
import re
import json
import secrets
import string
import shutil
import tempfile
import glob
from cryptography.fernet import Fernet, InvalidToken

# --- MED-2: Rutas absolutas ancladas al directorio del ejecutable ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KEY_FILE = os.path.join(BASE_DIR, "secret.key")
KEY_BACKUP = os.path.join(BASE_DIR, "secret.key.bak")
VAULT_DIR = os.path.join(BASE_DIR, "vaults")

# --- HIGH-4: Constantes para sanitización de nombres ---
INVALID_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
RESERVED_NAMES = (
    {'CON', 'PRN', 'AUX', 'NUL'}
    | {f'COM{i}' for i in range(1, 10)}
    | {f'LPT{i}' for i in range(1, 10)}
)

# --- MED-1: Límite máximo de tiempo de bloqueo (24 horas) ---
MAX_LOCK_MINUTES = 1440


def sanitize_vault_name(name):
    """HIGH-4: Valida y sanitiza el nombre de la bóveda contra path traversal y nombres reservados."""
    name = name.strip()
    if not name:
        raise ValueError("El nombre no puede estar vacío.")
    if INVALID_CHARS.search(name):
        raise ValueError("El nombre contiene caracteres no permitidos.")
    if name.upper() in RESERVED_NAMES:
        raise ValueError(f"'{name}' es un nombre reservado del sistema.")
    if '..' in name or '/' in name or '\\' in name:
        raise ValueError("El nombre contiene secuencias de ruta no permitidas.")
    if len(name) > 100:
        raise ValueError("El nombre es demasiado largo (máximo 100 caracteres).")
    return name


def initialize_system():
    """Inicializa el directorio de bóvedas y la clave maestra con backup redundante."""
    if not os.path.exists(VAULT_DIR):
        os.makedirs(VAULT_DIR)

    if not os.path.exists(KEY_FILE):
        # CRIT-3: Comprobar si existe un backup antes de crear clave nueva
        if os.path.exists(KEY_BACKUP):
            shutil.copy2(KEY_BACKUP, KEY_FILE)
        else:
            key = Fernet.generate_key()
            # Escritura atómica de la clave
            _atomic_write(KEY_FILE, key)
            # Crear backup inmediato
            shutil.copy2(KEY_FILE, KEY_BACKUP)
    else:
        # CRIT-3: Mantener backup sincronizado
        if not os.path.exists(KEY_BACKUP):
            shutil.copy2(KEY_FILE, KEY_BACKUP)
        else:
            _verify_key_backup()


def _verify_key_backup():
    """CRIT-3: Verifica que la clave y su backup coincidan. Repara si es necesario."""
    try:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
        with open(KEY_BACKUP, "rb") as f:
            backup = f.read()
        if key != backup:
            # La clave principal tiene prioridad
            shutil.copy2(KEY_FILE, KEY_BACKUP)
    except Exception:
        pass


def _atomic_write(filepath, data):
    """CRIT-1: Escritura atómica — escribe a temporal, sync, y renombra."""
    dir_path = os.path.dirname(filepath) or "."
    tmp_fd, tmp_path = tempfile.mkstemp(dir=dir_path, suffix=".tmp")
    try:
        with os.fdopen(tmp_fd, "wb") as tmp_file:
            tmp_file.write(data)
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
        os.replace(tmp_path, filepath)
    except Exception:
        # Limpiar temporal si falla
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def load_key():
    """Carga la clave maestra con fallback al backup."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
            if len(key) > 0:
                return key

    # CRIT-3: Fallback al backup
    if os.path.exists(KEY_BACKUP):
        with open(KEY_BACKUP, "rb") as backup_file:
            key = backup_file.read()
            if len(key) > 0:
                # Restaurar clave principal desde backup
                shutil.copy2(KEY_BACKUP, KEY_FILE)
                return key

    raise FileNotFoundError(
        "Clave maestra no encontrada (ni principal ni backup). "
        "Las bóvedas existentes no pueden desencriptarse."
    )


def generate_password(name, lock_time_minutes):
    """Genera una contraseña segura, la encripta y la guarda con verificación de integridad."""
    # HIGH-4: Sanitizar nombre
    name = sanitize_vault_name(name)

    # MED-1: Validar límite de tiempo
    if lock_time_minutes > MAX_LOCK_MINUTES:
        raise ValueError(f"El tiempo máximo de bloqueo es {MAX_LOCK_MINUTES} minutos (24 horas).")
    if lock_time_minutes <= 0:
        raise ValueError("El tiempo de bloqueo debe ser un número positivo.")

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

    # CRIT-1: Escritura atómica
    _atomic_write(vault_path, encrypted)

    # CRIT-2: Verificación post-escritura — releer y comprobar integridad
    try:
        verified_data = load_vault_info(name)
        if verified_data.get("password") != password:
            # Borrar archivo corrupto
            try:
                os.remove(vault_path)
            except OSError:
                pass
            raise RuntimeError(
                "Error de verificación: la contraseña guardada no coincide. "
                "La bóveda ha sido eliminada por seguridad. Inténtalo de nuevo."
            )
    except (ValueError, FileNotFoundError) as e:
        try:
            os.remove(vault_path)
        except OSError:
            pass
        raise RuntimeError(
            f"Error de verificación post-escritura: {e}. "
            "La bóveda ha sido eliminada por seguridad. Inténtalo de nuevo."
        )

    return password


def list_vaults():
    """Lista los nombres de las bóvedas disponibles."""
    if not os.path.exists(VAULT_DIR):
        return []
    vaults = glob.glob(os.path.join(VAULT_DIR, "*.vault"))
    return sorted([os.path.splitext(os.path.basename(v))[0] for v in vaults])


def load_vault_info(name):
    """HIGH-2: Carga y desencripta la bóveda con manejo de errores específico."""
    vault_path = os.path.join(VAULT_DIR, f"{name}.vault")
    if not os.path.exists(vault_path):
        raise FileNotFoundError(f"Bóveda '{name}' no encontrada.")

    key = load_key()
    f = Fernet(key)

    with open(vault_path, "rb") as vault_file:
        encrypted = vault_file.read()

    if len(encrypted) == 0:
        raise ValueError(f"La bóveda '{name}' está vacía (posible corrupción).")

    # HIGH-2: Excepciones específicas en vez de genérico
    try:
        decrypted = f.decrypt(encrypted)
    except InvalidToken:
        raise ValueError(
            f"No se puede desencriptar '{name}'. "
            "La clave maestra es incorrecta o la bóveda está corrupta. "
            "¿Se ha regenerado secret.key?"
        )

    try:
        data = json.loads(decrypted.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise ValueError(
            f"Bóveda '{name}' corrupta: datos internos ilegibles. ({e})"
        )

    # HIGH-3: Validar que el campo password existe y no está vacío
    if "password" not in data or not data["password"]:
        raise ValueError(
            f"Bóveda '{name}' corrupta: no contiene una contraseña válida."
        )

    return data


def delete_vault(name):
    """Elimina una bóveda del disco de forma segura."""
    vault_path = os.path.join(VAULT_DIR, f"{name}.vault")
    if not os.path.exists(vault_path):
        raise FileNotFoundError(f"Bóveda '{name}' no encontrada.")
    os.remove(vault_path)


def update_vault_time(name, new_lock_time_minutes):
    """Actualiza el tiempo de bloqueo de una bóveda existente, preservando la contraseña."""
    if new_lock_time_minutes <= 0:
        raise ValueError("El tiempo de bloqueo debe ser un número positivo.")
    if new_lock_time_minutes > MAX_LOCK_MINUTES:
        raise ValueError(f"El tiempo máximo de bloqueo es {MAX_LOCK_MINUTES} minutos (24 horas).")

    # Cargar datos actuales
    data = load_vault_info(name)
    password = data["password"]

    # Actualizar el tiempo
    data["lock_time_minutes"] = new_lock_time_minutes
    json_data = json.dumps(data)

    key = load_key()
    f = Fernet(key)
    encrypted = f.encrypt(json_data.encode('utf-8'))

    vault_path = os.path.join(VAULT_DIR, f"{name}.vault")

    # Escritura atómica
    _atomic_write(vault_path, encrypted)

    # Verificación post-escritura
    verified_data = load_vault_info(name)
    if verified_data.get("password") != password:
        raise RuntimeError("Error de verificación: la contraseña no coincide tras actualizar el tiempo.")
