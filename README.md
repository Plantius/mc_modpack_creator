# Minecraft Modpack Creator

A Python tool for creating and managing Minecraft modpacks. This program leverages the Modrinth API to streamline modpack creation, allowing for automatic mod updates, mod searches, and easy download of modpacks.

## Features

- **Automatic Mod Updates:** Keep your modpack up-to-date with the latest versions of your favorite mods.
- **Mod Search:** Search for new mods directly from the program.
- **Modpack Download:** Export your project as a complete, ready-to-use modpack.
- **Project Management:** Load, create, edit, and delete modpack projects easily.
- **Compatibility Check:** Ensure all mods within a modpack are compatible.

## Usage

### Running the Program

To run the Minecraft Modpack Creator, execute the following command:

```bash
python3 mc_mp/main.py [-h help] [-o project_to_load]
```

### Command-Line Options

- `-h, --help`: Display the help message with available options.
- `-o, --open_project <filename>`: Load an existing project by specifying the filename.

### Example

To load an existing project:

```bash
python3 mc_mp/main.py -o my_modpack.json
```

## Project Structure

- **modpack:** Contains modules related to project management and mod handling.
  - **mod.py:** Defines the `Mod` class, representing individual mods in a modpack.
  - **project.py:** Defines the `Project` class for handling modpack projects, including creation, loading, and saving.
- **args_parser:** Handles command-line arguments.
  - **args_parser.py:** Parses command-line arguments for the program.
- **menu:** Manages the user interface for interacting with modpack projects.
  - **main_menu.py:** Implements the main menu interface for navigating different options.
- **config:** Configuration files for default settings and API interactions.
  - **__init__.py:** Defines default API settings, headers, and filenames.

## Configuration

### Modpack Configuration

Located in the `modpack` package, this module defines key constants used throughout the application:

- **API_BASE:** Base URL for the Modrinth API.
- **HEADERS:** Default HTTP headers for API requests, including a custom `User-Agent`.
- **DEF_FILENAME:** Default filename for project files.

### Menu Configuration

In the `menu` package, configuration constants for user input are defined:

- **ACCEPT:** Default acceptance input (e.g., `'y'`).
- **REJECT:** Default rejection input (e.g., `'n'`).

## TODO

- Add `View mods` menu
- Validate user input more robustly.
- Expand the menu with additional options.
- Implement comprehensive tests.
- Improve CLI interface with more arguments.
- Add error handling for all input-dependent functions.

## Acknowledgements

- **[Simple Terminal Menu](https://pypi.org/project/simple-term-menu/):** Used for creating terminal-based menus.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).