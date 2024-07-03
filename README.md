# ssh-config-manager/README.md

# SSH Config Manager

This project provides a simple and efficient way to manage your SSH configurations using Make commands and a Python script.

## Prerequisites

- Python 3.10
- make

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/charles-adedotun/ssh-config-manager.git
   cd ssh-config-manager
   ```

2. Run the installation command:
   ```
   make install
   ```

   This command will attempt to install Python 3.10 using pyenv if it's not already on your system, create a virtual environment, install all required dependencies, and set up the SSH Config Manager.

3. Add the installation directory to your PATH if it's not already there:
   ```
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```
   (Use `~/.zshrc` instead of `~/.bashrc` if you're using Zsh)

4. If the automatic installation fails, you may need to install Python 3.10 manually. You can download it from [python.org](https://www.python.org/downloads/) or use pyenv. After installing Python 3.10, run `make install` again.

Note: This installation process does not require sudo privileges and installs the script in your user's home directory.

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