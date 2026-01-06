# create_dir

A command-line tool to create directories in a configured base path.

## Features

- **Command-line interface**: Accept directory names as command-line arguments
- **Persistent configuration**: Save base path in a configuration file
- **Interactive setup**: Prompts for base path on first use
- **Nested directory support**: Create parent directories automatically
- **Configuration management**: View current configuration with `--config` flag

## Installation

### From Source

```bash
git clone https://github.com/ErnieWhite/create_dir.git
cd create_dir
pip install -e .
```

After installation, you can use `create_dir` command directly.

### Without Installation

You can also run the script directly:

```bash
python3 create_dir.py <directory_name>
```

## Usage

### First Time Setup

When you run `create_dir` for the first time, it will prompt you for a base directory path:

```bash
$ create_dir my_project
Enter the base directory path: /home/user/projects
Configuration saved to /home/user/.config/create_dir.json
Created directory: /home/user/projects/my_project
```

### Creating Directories

After the initial setup, simply provide the directory name:

```bash
$ create_dir new_folder
Created directory: /home/user/projects/new_folder
```

### Creating Nested Directories

You can create nested directory structures:

```bash
$ create_dir project/src/components
Created directory: /home/user/projects/project/src/components
```

### Viewing Configuration

To see your current configuration:

```bash
$ create_dir --config dummy
Configuration file: /home/user/.config/create_dir.json
Base path: /home/user/projects
```

Note: When using `--config`, you still need to provide a directory argument (it will be ignored).

## Configuration

The configuration file is stored at `~/.config/create_dir.json` and contains:

```json
{
  "base_path": "/path/to/your/base/directory"
}
```

You can manually edit this file to change the base path.

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## How It Works

1. **Accepts a directory name** from the command line
2. **Loads the base path** from the configuration file (`~/.config/create_dir.json`)
3. **Prompts for base path** if the configuration file doesn't exist
4. **Saves the configuration** for future use
5. **Creates the directory** if it doesn't exist in the base path

## Testing

Run the test suite:

```bash
python3 -m unittest test_create_dir.py -v
```

## License

MIT License - see LICENSE file for details
