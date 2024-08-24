import sys, inspect, json
from cryptography.fernet import Fernet
import modpack.mod as mod

SECRET_KEY: bytes = "_Wentk-C_UTgkPQlUKoXQy_QGncHXgm8RoC4-ddWBG8="
MAGIC: bytes = b"MODPACK_PROJECT_CREATOR"

class ProjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, mod.Mod):
            return obj.export_json()
        return json.JSONEncoder.default(self, obj)


def get_variables(obj) -> dict:
    """Returns all variables in an object"""
    return {key:value for key, value in inspect.getmembers(obj) if not callable(getattr(obj, key)) and not key.startswith("__")}

def get_functions(obj) -> list:
    """"Returns all functions in an object"""
    return [i for i in dir(obj) if callable(getattr(obj, i)) and not i.startswith("__")]

def generate_id() -> str:
    f = Fernet(SECRET_KEY)
    return str(f.encrypt(MAGIC), "utf-8")

def check_id(id: str) -> bool:
    f = Fernet(SECRET_KEY)
    return f.decrypt(bytes(id, "utf-8")) == MAGIC

def get_input(msg: str) -> str:
    inp = str(input(msg))
    if not inp.isascii() or len(inp) == 0:
        eprint("[ERROR] Input contains non ASCII characters.")
        return None
    return inp

def get_index(lst: list, item) -> int:
    if item in lst:
        return lst.index(item)
    return None

def eprint(*args, **kwargs):
    """Print to stderr"""
    print(*args, file=sys.stderr, **kwargs)