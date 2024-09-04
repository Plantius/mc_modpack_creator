# MC Modpack Creator 🎮

MC Modpack Creator is a Python-based tool designed for creating and managing Minecraft modpacks. It provides functionality to define, load, save, and update modpacks while integrating with the Modrinth API for comprehensive mod information. The tool includes both a command-line interface (CLI) and an interactive terminal-based menu system for user convenience.

## Features ✨

Features include:

- **Create and Manage Projects**: Easily initialize, load, and save modpack projects.
- **Mod Management**: Add, remove, and update mods within a modpack.
- **Compatibility Checking**: Verify mod compatibility within your modpack.
- **Mod Search and Fetch**: Search for mods and retrieve detailed information using the Modrinth API.
- **Command-Line Interface**: Directly manage projects and mods via the command line.
- **Interactive Menu System**: Use an intuitive terminal-based menu to navigate and manage your modpack.

## Installation 🛠️

Installation instructions include:

### Prerequisites

List of required prerequisites:

- Python 3.7 or later
- Required Python packages (listed below)

### Clone the Repository

Steps to clone the repository:

```bash
git clone https://github.com/Plantius/mc_modpack_creator.git
cd mc_modpack_creator
```

### Install Dependencies

Command to install necessary dependencies:

```bash
pip install -r requirements.txt
```

### Setup

Instructions for setting up the project:

Configure your **SECRET_KEY** in **standard.py** for encryption and decryption of project IDs. Replace the placeholder with a securely generated key.

## Usage 🚀

Instructions for using the tool:

### Command-Line Interface

Commands available in the CLI:

```plaintext
-o, --open_project: Specify the project file to load.
-c, --create_project: Specify the name of the new project to create.
-l, --list_projects: List all available projects.
-d, --delete_project: Specify the project file to delete.
-m, --list_mods: List all mods in the current project.
--menu_disable: Disable the project menu.
```

### Interactive Menu

The interactive terminal-based menu system allows you to:

```plaintext
Load, save, and create projects.
Add, remove, and update mods.
Change project settings.
List current mods.
```
## Credit
- Simple term menu <https://pypi.org/project/simple-term-menu/>

## Documentation
See <https://plantius.github.io/mc_modpack_creator/>.

## License 📜

This project is licensed under the MIT License. See the LICENSE file for details.
Contributing 🤝

Contributions are welcome! Please see the CONTRIBUTING guidelines for more information.
Contact 📫

For any questions or issues, please open an issue on the GitHub repository or contact Plantius.

Happy modding! 🎉
