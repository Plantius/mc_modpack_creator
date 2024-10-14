"""
Author: Plantius (https://github.com/Plantius)
Filename: ./mc_mp/standard.py
Last Edited: 2024-09-10

This module is part of the MC Modpack Creator project. For more details, visit:
https://github.com/Plantius/mc_modpack_creator
"""
from mc_mp.constants import BUF_SIZE
from enum import Enum, auto
import os
import sys
import inspect
import zipfile
import hashlib
import time 
import functools
import uuid

class Setting(Enum):
    TITLE = auto()
    DESCRIPTION = auto()    
    MC_VERSION= auto()    
    MOD_LOADER = auto()    
    BUILD_VERSION = auto()   
    CLIENT_SIDE = auto() 
    SERVER_SIDE = auto() 

debug_flag = False

def set_debug_flag(enable: bool) -> None:
    """
    Enables or disables debug flag, which controls timing wrappers and other debug functionality.
    """
    global debug_flag
    debug_flag = enable

def is_debug_flag() -> bool:
    """
    Returns whether the debug flag is enabled or not.
    """
    return debug_flag

def async_timing(func):
    """Decorator to measure the execution time of an async function."""
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if not is_debug_flag():
            return await func(*args, **kwargs)
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
        if not is_debug_flag():
            return func(*args, **kwargs)
        start_time = time.monotonic()  # Start time measurement
        result = func(*args, **kwargs)
        end_time = time.monotonic()  # End time measurement
        duration = end_time - start_time
        print(f"[TIMER] {func.__name__} executed in {duration:.4f} seconds")
        return result
    
    return wrapper


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
    """Generates a unique project ID using UUID4."""
    project_id = str(uuid.uuid4())
    return project_id

def is_valid_project_id(project_id: str) -> bool:
    """Checks if the provided project ID is a valid UUID4."""
    try:
        uuid_obj = uuid.UUID(project_id, version=4)
        return str(uuid_obj) == project_id
    except ValueError:
        return False

def get_input(msg: str) -> str:
    """Prompt for ASCII input and return it if valid."""
    inp = input(msg)
    if not inp.isascii() or inp is None:
        eprint("[ERROR] Input must be a non-empty ASCII string.")
        return ""
    return inp

def get_index(lst: list, item) -> int:
    """Return the index of an item in the list, or `None` if not found."""
    try:
        return lst.index(item)
    except ValueError:
        return -1

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

def zip_dir(filename: str, mp_dir: str):
    with zipfile.ZipFile(f"{filename}.mrpack", "w") as file:
        for root, subdirs, files in os.walk(mp_dir):
            cur_dir = root[len(mp_dir):]
            for filename in files:
                file.write(os.path.join(root, filename), os.path.join(cur_dir, filename))
