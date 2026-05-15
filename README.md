# Archive Tool

A command-line tool for archiving user files based on Linux user groups.

## Features
- Archive files by Linux user group
- Configurable target directories
- CLI-based execution
- Debian package support (.deb)

## Installation
```bash
1. wget https://github.com/Infrablue1984/archive-tool/archive/refs/tags/v1.0.1.tar.gz
2. tar -xzf v1.0.1.tar.gz
3. cd archive-tool-1.0.1
4. sudo dpkg -i build/archive-tool.deb
```

## Usage
```bash
archive-tool <group-name>
```

## Requirements
- Python 3.12+
- Linux (Debian-based systems)
