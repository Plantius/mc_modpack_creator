import sys
from cryptography.fernet import Fernet

SECRET_KEY: bytes = "_Wentk-C_UTgkPQlUKoXQy_QGncHXgm8RoC4-ddWBG8="
MAGIC: bytes = b"MODPACK_PROJECT_CREATOR"

def get_variables(obj) -> dict:
    """Returns all variables in an object"""
    return {key:value for key, value in obj.__dict__.items() if not key.startswith('__') and not callable(key)}

def get_functions(obj) -> list:
    """"Returns all functions in an object"""
    return [i for i in dir(obj) if callable(getattr(obj, i)) and not i.startswith("__")]

def generate_id() -> str:
    f = Fernet(SECRET_KEY)
    return str(f.encrypt(MAGIC), "utf-8")

def check_id(id: str) -> bool:
    f = Fernet(SECRET_KEY)
    return f.decrypt(bytes(id, "utf-8")) == MAGIC

def eprint(*args, **kwargs):
    """Print to stderr"""
    print(*args, file=sys.stderr, **kwargs)