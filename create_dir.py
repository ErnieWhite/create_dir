#!/usr/bin/env python3
"""
Command-line tool to create directories in a configured base path.
"""
import argparse
import json
import os
import sys
from pathlib import Path


def get_config_file_path():
    """
    Get the path to the configuration file.
    The config file has the same name as the program.
    """
    program_name = Path(sys.argv[0]).stem
    # Handle edge cases like 'python3 -m unittest', '-c', etc.
    # Check if the program name contains any of these patterns
    invalid_patterns = ['python', 'pytest', '__main__', 'unittest', '-c', '-m']
    if not program_name or any(pattern in program_name for pattern in invalid_patterns):
        program_name = 'create_dir'
    config_dir = Path.home() / '.config'
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / f'{program_name}.json'


def load_config():
    """
    Load the configuration from the config file.
    Returns None if the config file doesn't exist.
    """
    config_file = get_config_file_path()
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading config file: {e}", file=sys.stderr)
            return None
    return None


def save_config(config):
    """
    Save the configuration to the config file.
    """
    config_file = get_config_file_path()
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        print(f"Configuration saved to {config_file}")
    except IOError as e:
        print(f"Error saving config file: {e}", file=sys.stderr)
        sys.exit(1)


def prompt_for_base_path():
    """
    Prompt the user for the base directory path.
    """
    while True:
        base_path = input("Enter the base directory path: ").strip()
        if not base_path:
            print("Base path cannot be empty. Please try again.")
            continue
        
        base_path_obj = Path(base_path).expanduser().resolve()
        
        # Check if the path exists
        if not base_path_obj.exists():
            create = input(f"Directory '{base_path_obj}' does not exist. Create it? (y/n): ").strip().lower()
            if create == 'y':
                try:
                    base_path_obj.mkdir(parents=True, exist_ok=True)
                    print(f"Created base directory: {base_path_obj}")
                except OSError as e:
                    print(f"Error creating directory: {e}", file=sys.stderr)
                    continue
            else:
                print("Please enter a different path.")
                continue
        
        # Check if it's a directory
        if not base_path_obj.is_dir():
            print(f"Error: '{base_path_obj}' is not a directory.", file=sys.stderr)
            continue
        
        return str(base_path_obj)


def get_base_path():
    """
    Get the base path from config or prompt the user.
    """
    config = load_config()
    
    if config and 'base_path' in config:
        base_path = config['base_path']
        # Verify the base path still exists
        if Path(base_path).exists():
            return base_path
        else:
            print(f"Warning: Configured base path '{base_path}' no longer exists.")
    
    # Config doesn't exist or base path is invalid, prompt user
    base_path = prompt_for_base_path()
    save_config({'base_path': base_path})
    return base_path


def create_directory(base_path, dir_name):
    """
    Create a directory in the base path.
    """
    target_path = Path(base_path) / dir_name
    
    if target_path.exists():
        if target_path.is_dir():
            print(f"Directory already exists: {target_path}")
            return True
        else:
            print(f"Error: '{target_path}' exists but is not a directory.", file=sys.stderr)
            return False
    
    try:
        target_path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {target_path}")
        return True
    except OSError as e:
        print(f"Error creating directory: {e}", file=sys.stderr)
        return False


def main():
    """
    Main entry point for the program.
    """
    parser = argparse.ArgumentParser(
        description='Create a directory in a configured base path.'
    )
    parser.add_argument(
        'directory',
        help='Name of the directory to create'
    )
    parser.add_argument(
        '--config',
        action='store_true',
        help='Show the current configuration'
    )
    
    args = parser.parse_args()
    
    # Show config if requested
    if args.config:
        config = load_config()
        if config:
            config_file = get_config_file_path()
            print(f"Configuration file: {config_file}")
            print(f"Base path: {config.get('base_path', 'Not set')}")
        else:
            print("No configuration found.")
        return
    
    # Get base path (will prompt if not configured)
    base_path = get_base_path()
    
    # Create the directory
    if create_directory(base_path, args.directory):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
