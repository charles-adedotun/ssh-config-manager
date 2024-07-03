# ssh-config-manager/README.md

# SSH Config Manager

This project provides a simple and efficient way to manage your SSH configurations using Make commands and a Python script.

## Prerequisites

- Python 3.6+
- make

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ssh-config-manager.git
   cd ssh-config-manager
   ```

2. Install the SSH Config Manager:
   ```
   make install
   ```

## Usage

Use the following Make commands to manage your SSH configurations:

- `make add`: Add a new SSH config entry
- `make list`: List all SSH config entries
- `make remove`: Remove an SSH config entry
- `make backup`: Create a backup of the current SSH config
- `make restore`: Restore a previous SSH config backup
- `make help`: Show all available commands

## Features

- Colorful output for better readability
- Interactive prompts for adding and removing configurations
- Automatic backup creation before making changes
- Easy restoration of previous configurations

## Uninstallation

To uninstall the SSH Config Manager:

```
make uninstall
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.