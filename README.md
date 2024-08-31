# MC Modpack Creator Project Documentation

## Overview
The MC Modpack Creator project is a tool for managing Minecraft modpacks, including mod information, compatibility checks, and API interactions with the Modrinth API. This documentation covers the main classes and methods within the project, providing details on their usage and functionality.

## Project Class (`project.py`)

### Description
The `Project` class is responsible for managing Minecraft modpack projects, including loading, saving, adding, and removing mods, as well as interacting with external APIs for mod information.

### Attributes
- `modpack: Modpack`: Instance of the `Modpack` class, representing the current modpack.
- `api: ProjectAPI`: Instance of the `ProjectAPI` class for interacting with the Modrinth API.
- `metadata: Dict[str, Any]`: Dictionary storing metadata about the project, including whether it is loaded, saved, the filename, and the project ID.

### Methods

- `__init__(self, **kwargs) -> None`: Initializes a `Project` instance and `ProjectAPI`.
  
- `is_mod_installed(self, id: str) -> int`: Checks if a mod is installed by ID and returns its index.

- `create_project(self, **kwargs) -> None`: Creates a new project, updates metadata, and checks modpack compatibility.

- `load_project(self, filename: str) -> bool`: Loads project data from a file and initializes the modpack.

- `save_project(self, filename: Optional[str] = DEF_FILENAME) -> bool`: Saves the current project state to a file.

- `search_mods(self, **kwargs) -> dict`: Searches for mods using the `ProjectAPI`.

- `add_mod(self, name: str, version: dict, project_info: dict, index: int = 0) -> bool`: Adds a mod to the modpack with the given name and version information.

- `rm_mod(self, index: int) -> bool`: Removes a mod from the modpack by index.

- `update_mod(self, selected_index: list[int]) -> bool`: Updates selected mods if newer versions are available.

- `list_projects(self) -> list[str]`: Lists all valid projects with their filenames and descriptions.

- `list_mods(self) -> list[str]`: Lists all mods in the loaded project with their names and descriptions.

- `fetch_mods_by_ids(self, ids: list[str]) -> list[dict]`: Fetches mods by their IDs concurrently and returns detailed information.

## Modpack Class (`modpack.py`)

### Description
The `Modpack` class represents a Minecraft modpack, providing methods to manage mods, export modpack data, and check compatibility.

### Attributes
- `title: str`: Title of the modpack.
- `description: str`: Description of the modpack.
- `build_date: str`: Date the modpack was built.
- `build_version: str`: Version of the modpack build.
- `mc_version: str`: Minecraft version used by the modpack.
- `mod_loader: str`: Mod loader used by the modpack (e.g., "fabric").
- `client_side: str`: Specifies if the mod is required on the client side.
- `server_side: str`: Specifies if the mod is required on the server side.
- `mod_data: list[Mod]`: List of mods included in the modpack.

### Methods

- `__init__(self, **kwargs: Any) -> None`: Initializes the Modpack with optional parameters.

- `export_json(self) -> Dict[str, Any]`: Exports the Modpack attributes as a JSON-compatible dictionary.

- `check_compatibility(self) -> bool`: Checks if the mods in the modpack are compatible (always returns True).

- `get_mods_name_ver(self) -> List[str]`: Returns a list of all mod names and their version numbers.

- `get_mods_descriptions(self) -> List[str]`: Returns a list of all mod descriptions.

## Mod Class (`mod.py`)

### Description
The `Mod` class represents a Minecraft mod with attributes and methods for JSON serialization and deserialization.

### Attributes
- `title: str`: Title of the mod.
- `description: str`: Description of the mod.
- `name: str`: Name of the mod version.
- `changelog: str`: Changelog for the mod version.
- `version_number: str`: Version number of the mod.
- `dependencies: list[dict]`: List of dependencies required by the mod.
- `mc_versions: list`: List of Minecraft versions compatible with the mod.
- `version_type: str`: Type of the mod version (e.g., "release").
- `mod_loaders: list`: List of mod loaders compatible with the mod.
- `id: str`: Unique ID of the mod version.
- `project_id: str`: Unique ID of the mod project.
- `date_published: str`: Date the mod version was published.
- `files: list[dict]`: List of files associated with the mod version.

### Methods

- `export_json(self) -> dict`: Exports the mod's attributes as a JSON-compatible dictionary.

- `load_json(self, data: dict) -> None`: Loads JSON data into the mod's attributes.

## ProjectAPI Class (`project_api.py`)

### Description
The `ProjectAPI` class handles interactions with the Modrinth API for project-related data, including fetching project details, versions, and dependencies.

### Methods

- `request(endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]`: Makes a GET request to the specified API endpoint and returns the JSON response.

- `parse_url(params: Dict[str, Any]) -> str`: Converts a dictionary of parameters into a URL query string.

- `is_slug_valid(slug_or_id: str) -> Optional[Dict[str, Any]]`: Checks if the given project name or ID exists on Modrinth.

- `get_dependencies(project_name: str) -> Optional[Dict[str, Any]]`: Retrieves all dependencies for the specified project.

- `search_project(**kwargs) -> Optional[Dict[str, Any]]`: Searches for projects with various filters and sorting options.

- `get_project(project_name: str) -> Optional[Dict[str, Any]]`: Retrieves detailed information about a specific project.

- `get_projects(**kwargs) -> Optional[Dict[str, Any]]`: Retrieves information about multiple projects.

- `list_versions(**kwargs) -> Optional[Dict[str, Any]]`: Lists versions of a specified project with optional filtering.

- `get_version(version_id: str) -> Optional[Dict[str, Any]]`: Retrieves detailed information about a specific version by its ID.

- `get_versions(**kwargs) -> Optional[Dict[str, Any]]`: Retrieves information about multiple versions by their IDs.
