# MC Modpack Creator 🎮

MC Modpack Creator is a Python-based tool for creating and managing Minecraft modpacks. It allows users to define, load, save, and update modpacks, integrating with the Modrinth API for mod information. This tool includes a command-line interface and a terminal-based menu system for ease of use.

## Features ✨

- **Create and Manage Projects**: Initialize, load, and save modpack projects.
- **Mod Management**: Add, remove, and update mods within a modpack.
- **Compatibility Checking**: Ensure mod compatibility within a modpack.
- **Mod Search and Fetch**: Search for mods and fetch detailed mod information from the Modrinth API.
- **Command-Line Interface**: Manage projects and mods directly from the command line.
- **Interactive Menu System**: Navigate and manage your modpack using an intuitive terminal-based menu.

## Installation 🛠️

### Prerequisites

- Python 3.7 or later
- Required Python packages (listed below)

### Clone the Repository

```bash
git clone https://github.com/Plantius/mc_modpack_creator.git
cd mc_modpack_creator
```

### Install Dependencies

```bash
pip install -r requirements.txt
```
### Setup

Configure your **SECRET_KEY** in **standard.py** for encryption and decryption of project IDs. Replace the placeholder with a securely generated key.

## Usage 🚀
### Command-Line Interface

The tool includes a command-line interface (CLI) for managing projects and mods. Below are the available commands:

    -o, --open_project: Specify the project file to load.
    -c, --create_project: Specify the name of the new project to create.
    -l, --list_projects: List all available projects.
    -d, --delete_project: Specify the project file to delete.
    -m, --list_mods: List all mods in the current project.
    --menu_disable: Disable the project menu.

### Interactive Menu

The tool also includes an interactive terminal-based menu system to manage your modpack. The main menu provides options to:

    Load, save, and create projects.
    Add, remove, and update mods.
    Change project settings.
    List current mods.

## License 📜

This project is licensed under the MIT License. See the LICENSE file for details.
Contributing 🤝

Contributions are welcome! Please see the CONTRIBUTING guidelines for more information.
Contact 📫

For any questions or issues, please open an issue on the GitHub repository or contact Plantius.

Happy modding! 🎉