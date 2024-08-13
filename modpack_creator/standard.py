def get_variables(class_obj) -> list:
    return [i for i in dir(class_obj) if not callable(getattr(class_obj, i)) and not i.startswith("__")]