import os
from datetime import datetime

HEADER_TEMPLATE_PATH = 'header_template.txt'
FILES_DIRECTORY = './mc_mp'  # Adjust this to the directory containing your Python files

def get_header(file_path):
    with open(HEADER_TEMPLATE_PATH, 'r') as file:
        template = file.read()
    date_str = datetime.now().strftime('%Y-%m-%d')
    return template.format(date=date_str, file=file_path)

def update_file_header(file_path):
    header = get_header(file_path)
    with open(file_path, 'r') as file:
        content = file.read()

    if content.startswith('"""'):
        # If header already exists, replace it
        end_of_header = content.find('"""', 3) + 3
        content = header + content[end_of_header:]
    else:
        # Insert header at the top
        content = header + '\n' + content

    with open(file_path, 'w') as file:
        file.write(content)

def update_headers(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):  # Update only Python files
                file_path = os.path.join(root, file)
                update_file_header(file_path)

if __name__ == "__main__":
    update_headers(FILES_DIRECTORY)
