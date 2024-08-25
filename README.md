# Minecraft Modpack Creator

A Python tool for creating and managing Minecraft modpacks. This program leverages the Modrinth API to streamline modpack creation, allowing for automatic mod updates, mod searches, and easy download of modpacks.

## Features

- **Automatic Mod Updates:** Keep your modpack up-to-date with the latest versions of your favorite mods.
- **Mod Search:** Search for new mods directly from the program.
- **Modpack Download:** Export your project as a complete, ready-to-use modpack.
- **Project Management:** Load, create, edit, delete, and list modpack projects easily.
- **Mod Management:** Add or remove mods from your project.
- **Compatibility Check:** Ensure all mods within a modpack are compatible.

## Usage

### Running the Program

To run the Minecraft Modpack Creator, execute the following command:

    python3 mc_mp/main.py [options]

### Command-Line Options

- `-h, --help`: Display the help message with available options.
- `-o, --open_project <filename>`: Load an existing project by specifying the filename.
- `-c, --create_project <name>`: Create a new project with the specified name.
- `-l, --list_projects`: List all available projects.
- `-d, --delete_project <filename>`: Delete the specified project file.
- `-m, --list_mods`: List all mods in the current project.
- `--menu`: Launch the project menu directly.

### Examples

- To load an existing project:
    ```
    python3 mc_mp/main.py -o my_modpack.json
    ```

- To create a new project:
    ```
    python3 mc_mp/main.py -c my_new_modpack
    ```

- To list all available projects:
    ```
    python3 mc_mp/main.py -l
    ```

- To delete a project:
    ```
    python3 mc_mp/main.py -d my_modpack.json
    ```

- To list all mods in the current project:
    ```
    python3 mc_mp/main.py -m
    ```

- To open the project menu directly:
    ```
    python3 mc_mp/main.py --menu
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
