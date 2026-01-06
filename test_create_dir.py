#!/usr/bin/env python3
"""
Test suite for create_dir.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestCreateDir(unittest.TestCase):
    """Test cases for create_dir functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / '.config'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / 'create_dir.json'
        
        # Create a base path for testing
        self.base_path = Path(self.test_dir) / 'base'
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Save the original HOME
        self.original_home = os.environ.get('HOME')
        # Set HOME to test directory
        os.environ['HOME'] = self.test_dir
        
    def tearDown(self):
        """Clean up test fixtures."""
        # Restore original HOME
        if self.original_home:
            os.environ['HOME'] = self.original_home
        else:
            os.environ.pop('HOME', None)
        
        # Remove test directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_config_file_creation(self):
        """Test that config file is created with correct path."""
        # Import after setting up environment
        sys.path.insert(0, '/home/runner/work/create_dir/create_dir')
        # Force reload to get updated code
        if 'create_dir' in sys.modules:
            import importlib
            import create_dir
            importlib.reload(create_dir)
        else:
            import create_dir
        
        config_path = create_dir.get_config_file_path()
        self.assertTrue(str(config_path).endswith('create_dir.json'))
    
    def test_save_and_load_config(self):
        """Test saving and loading configuration."""
        sys.path.insert(0, '/home/runner/work/create_dir/create_dir')
        import create_dir
        
        test_config = {'base_path': str(self.base_path)}
        create_dir.save_config(test_config)
        
        loaded_config = create_dir.load_config()
        self.assertIsNotNone(loaded_config)
        self.assertEqual(loaded_config['base_path'], str(self.base_path))
    
    def test_create_directory(self):
        """Test directory creation."""
        sys.path.insert(0, '/home/runner/work/create_dir/create_dir')
        import create_dir
        
        dir_name = 'test_directory'
        result = create_dir.create_directory(str(self.base_path), dir_name)
        
        self.assertTrue(result)
        target_path = self.base_path / dir_name
        self.assertTrue(target_path.exists())
        self.assertTrue(target_path.is_dir())
    
    def test_create_directory_already_exists(self):
        """Test that creating an existing directory succeeds."""
        sys.path.insert(0, '/home/runner/work/create_dir/create_dir')
        import create_dir
        
        dir_name = 'existing_directory'
        target_path = self.base_path / dir_name
        target_path.mkdir()
        
        result = create_dir.create_directory(str(self.base_path), dir_name)
        self.assertTrue(result)
    
    def test_create_nested_directory(self):
        """Test creating nested directories."""
        sys.path.insert(0, '/home/runner/work/create_dir/create_dir')
        import create_dir
        
        dir_name = 'parent/child/grandchild'
        result = create_dir.create_directory(str(self.base_path), dir_name)
        
        self.assertTrue(result)
        target_path = self.base_path / dir_name
        self.assertTrue(target_path.exists())
        self.assertTrue(target_path.is_dir())
    
    def test_command_line_with_config(self):
        """Test command line execution with existing config."""
        # Create config file
        config = {'base_path': str(self.base_path)}
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
        
        # Run the script
        result = subprocess.run(
            [sys.executable, '/home/runner/work/create_dir/create_dir/create_dir.py', 'cmdline_test'],
            cwd='/home/runner/work/create_dir/create_dir',
            capture_output=True,
            text=True,
            env={**os.environ, 'HOME': self.test_dir}
        )
        
        self.assertEqual(result.returncode, 0)
        target_path = self.base_path / 'cmdline_test'
        self.assertTrue(target_path.exists())
    
    def test_show_config(self):
        """Test --config flag to show configuration."""
        # Create config file
        config = {'base_path': str(self.base_path)}
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
        
        # Run the script with --config
        result = subprocess.run(
            [sys.executable, '/home/runner/work/create_dir/create_dir/create_dir.py', '--config', 'dummy'],
            cwd='/home/runner/work/create_dir/create_dir',
            capture_output=True,
            text=True,
            env={**os.environ, 'HOME': self.test_dir}
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('Base path:', result.stdout)
        self.assertIn(str(self.base_path), result.stdout)


if __name__ == '__main__':
    unittest.main()
