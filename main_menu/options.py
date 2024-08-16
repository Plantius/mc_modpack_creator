def load_project() -> bool:
    """Loads a project"""
    print("Please enter a project filename: ")
    filename = str(input())
    if not filename.isalnum():
        print("Filename contains non-ASCII characters.")
        return False
    
    
    return True