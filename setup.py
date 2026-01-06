#!/usr/bin/env python3
"""Setup script for create_dir CLI tool."""
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="create_dir",
    version="1.0.0",
    author="Ernie White",
    description="A command-line tool to create directories in a configured base path",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ErnieWhite/create_dir",
    py_modules=["create_dir"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "create_dir=create_dir:main",
        ],
    },
)
