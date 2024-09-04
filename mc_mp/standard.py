"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/standard.py
Last Edited: 2024-08-31

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
import sys
import os
import inspect
import json
import glob
from cryptography.fernet import Fernet
import modpack.mod as mod
import hashlib
import time 
import functools

BUF_SIZE = 2 << 15
SECRET_KEY = b'7rfdYCctHr9xCK2H4i92HLvxN4YzsTty4OrNaAC-bfc='
UNIQUE_ID = "MC_MODPACK_CREATOR_ID"

cipher = Fernet(SECRET_KEY)

ALLOWED_CATEGORIES = ["forge", "fabric", "neoforge", "quilt", "liteloader"]

def async_timing(func):
    """Decorator to measure the execution time of an async function."""
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.monotonic()  # Start time measurement
        result = await func(*args, **kwargs)
        end_time = time.monotonic()  # End time measurement
        duration = end_time - start_time
        print(f"[TIMER] {func.__name__} executed in {duration:.4f} seconds")
        return result
    
    return wrapper

def sync_timing(func):
    """Decorator to measure the execution time of a synchronous function."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()  # Start time measurement
        result = func(*args, **kwargs)
        end_time = time.monotonic()  # End time measurement
        duration = end_time - start_time
        print(f"[TIMER] {func.__name__} executed in {duration:.4f} seconds")
        return result
    
    return wrapper

class ProjectEncoder(json.JSONEncoder):
    """Custom JSON encoder for handling `mod.Mod` objects."""

    def default(self, obj):
        """Encode `mod.Mod` objects to JSON; use default encoder otherwise."""
        if isinstance(obj, mod.Mod):
            return obj.export_json()
        return super().default(obj)

def get_variables(obj) -> dict:
    """Get non-callable attributes of an object as a dictionary."""
    return {key: value for key, value in inspect.getmembers(obj) 
            if not callable(getattr(obj, key)) and not key.startswith("__")
            and not key.startswith("_")}

def get_functions(obj) -> list:
    """Get a list of callable methods, excluding special methods."""
    return [name for name in dir(obj) 
            if callable(getattr(obj, name)) and not name.startswith("__")]

def generate_project_id() -> str:
    """Generates and encrypts a new project ID."""
    project_id = UNIQUE_ID
    return cipher.encrypt(project_id.encode()).decode()

def is_valid_project_id(encrypted_id: str) -> bool:
    """Checks if the provided encrypted project ID is valid."""
    try:
        decrypted_id = cipher.decrypt(encrypted_id.encode()).decode()
        return decrypted_id == UNIQUE_ID
    except:
        return False

def get_input(msg: str) -> str:
    """Prompt for ASCII input and return it if valid."""
    inp = input(msg)
    if not inp.isascii() or inp is None:
        eprint("[ERROR] Input must be a non-empty ASCII string.")
        return None
    return inp

def get_index(lst: list, item) -> int:
    """Return the index of an item in the list, or `None` if not found."""
    try:
        return lst.index(item)
    except ValueError:
        return None

def get_project_files() -> list:
    """Returns a sorted list of JSON files in the current directory."""
    return sorted(glob.glob("./*.json"))

def has_duplicates(lst: list) -> bool:
    """Check if there are duplicates in the list."""
    return len(lst) != len(set(lst))

def eprint(*args, **kwargs) -> None:
    """Print errors to standard error."""
    print(*args, file=sys.stderr, **kwargs)

def check_hash(filename: str, hashes: dict) -> bool:
    sha1 = hashlib.sha1()
    sha512 = hashlib.sha512()
    with open(filename, 'rb') as file:
        while True:
            data = file.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
            sha512.update(data)
    return sha1.hexdigest() == hashes["sha1"] and sha512.hexdigest() == hashes["sha512"]
