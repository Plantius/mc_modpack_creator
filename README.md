# Minecraft Modpack Creator

A Python tool for creating Minecraft modpacks. It integrates with the Modrinth API to automate mod updates and manage modpack creation.

## Features

- **Automatic Mod Updates**: Keep your mods up to date effortlessly.
- **Mod Search**: Easily find new mods to include in your modpack.
- **Complete Modpack Download**: Download your modpack as a single, ready-to-use file.

## Usage

Run the main script with optional arguments:

```sh
python3 mc_mp/main.py [-h] [-o project_to_load]
```

- `-h, --help`: Display help information.
- `-o project_to_load`: Specify the project file to load.

## TODO

- Validate user input
- Expand menu options
- Develop tests
- Add CLI argument support
- Implement comprehensive error handling

## Acknowledgements

- [Simple Terminal Menu](https://pypi.org/project/simple-term-menu/) for terminal menu functionality.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).