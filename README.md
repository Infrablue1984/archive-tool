# Archive Tool

A command-line tool for archiving user files based on Linux user groups.

## Features
- Archive files by Linux user group while preserving the original directory structure.
- Configurable target archive directory.
- Events and results to a log file.
- Thread Save
- CLI-based execution
- Debian package support (.deb)

## Installation

### From the Debian package

Download the latest release from GitHub and install the `.deb` file:

```bash
sudo dpkg -i archive-tool.deb
```

### From source

```bash
git clone https://github.com/Infrablue1984/archive-tool.git
cd archive-tool
```

To build the Debian package locally, run:

```bash
dpkg-deb --build archive-tool
```

## Usage
```bash
archive-tool <group-name>
```

Example:

```bash
archive-tool developers
```

## Project structure
This repository contains the Python source code and the Debian packaging files used to build the package.

- `archive-tool/DEBIAN/control` Debian control file.
- `archive-tool/opt/archive-tool` Python files
  - `archive-tool/opt/archive-tool/file_archiver.py` Main file for archiving files.
  - `archive-tool/opt/archive-tool/config.py` File to configure target archive directory.
  - `archive-tool/opt/archive-tool/log.json` File to set logging configuration and directory.
  - `archive-tool/opt/archive-tool/log_config.py` File to handle logging.
  - `archive-tool/opt/archive-tool/lock.py` File to handle locks.
- `archive-tool/usr/local/bin/archive-tool` Entry point to run application.


## Requirements
- Python 3.12+
- Linux (Debian-based systems)
  
## License

MIT License.
