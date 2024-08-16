def get_variables(obj) -> list:
    """Returns all variables in an object"""
    return [i for i in dir(obj) if not callable(getattr(obj, i)) and not i.startswith("__")]

def get_functions(obj) -> list:
    """"Returns all functions in an object"""
    return [i for i in dir(obj) if callable(getattr(obj, i)) and not i.startswith("__")]

def get_list(mapped_list, inp):
    for key in mapped_list:
        if key[0] <= inp <= key[1]:
            return mapped_list[key]