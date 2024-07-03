#!/usr/bin/env python3

# ssh_config_manager.py

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List
import logging
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.styles import Style
from colorama import init, Fore, Style as ColoramaStyle

# Initialize colorama for cross-platform color support
init()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
CONFIG_DIR = Path.home() / ".ssh_config_manager"
SSH_CONFIG_PATH = Path.home() / ".ssh" / "config"
BACKUP_DIR = CONFIG_DIR / "backups"

# Ensure necessary directories exist
CONFIG_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)

# Prompt toolkit styles
dialog_style = Style.from_dict({
    'dialog': 'bg:#88ff88',
    'dialog frame.label': 'bg:#ffffff #000000',
    'dialog.body': 'bg:#000000 #00ff00',
    'dialog shadow': 'bg:#00aa00',
})

def load_config() -> Dict[str, Any]:
    """Load the configuration from the JSON file."""
    config_path = CONFIG_DIR / "config.json"
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}

def save_config(config: Dict[str, Any]) -> None:
    """Save the configuration to the JSON file."""
    config_path = CONFIG_DIR / "config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

def backup_ssh_config() -> Path:
    """Create a backup of the current SSH config file."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"config_{timestamp}.bak"
    import shutil
    shutil.copy(SSH_CONFIG_PATH, backup_path)
    logger.info(f"Backed up SSH config to {backup_path}")
    return backup_path

def update_ssh_config(host: str, config: Dict[str, str]) -> None:
    """Update the SSH config file with new or modified host information."""
    backup_ssh_config()
    
    with open(SSH_CONFIG_PATH, 'r') as f:
        lines = f.readlines()

    host_index = next((i for i, line in enumerate(lines) if line.strip().startswith(f"Host {host}")), None)

    new_config = [f"Host {host}\n"]
    for key, value in config.items():
        new_config.append(f"    {key} {value}\n")
    new_config.append("\n")

    if host_index is not None:
        end_index = next((i for i in range(host_index + 1, len(lines)) if not lines[i].strip().startswith(" ")), len(lines))
        lines[host_index:end_index] = new_config
    else:
        lines.extend(new_config)

    with open(SSH_CONFIG_PATH, 'w') as f:
        f.writelines(lines)

    logger.info(f"Updated SSH config for host {host}")

def add_config() -> None:
    """Add a new SSH config entry interactively."""
    config = load_config()
    
    host = prompt("Enter host name: ")
    hostname = prompt("Enter hostname or IP: ")
    user = prompt("Enter username: ")
    identity_file = prompt("Enter identity file path: ", default=str(Path.home() / ".ssh" / "id_rsa"))

    update_ssh_config(host, {
        "HostName": hostname,
        "User": user,
        "IdentityFile": identity_file
    })

    save_config(config)
    print(Fore.GREEN + f"Added SSH config for host {host}" + ColoramaStyle.RESET_ALL)

def list_configs() -> None:
    """List all SSH config entries."""
    with open(SSH_CONFIG_PATH, 'r') as f:
        content = f.read()
        print(Fore.CYAN + "Current SSH Configurations:" + ColoramaStyle.RESET_ALL)
        print(content)

def get_hosts() -> List[str]:
    """Get a list of all hosts from the SSH config file."""
    with open(SSH_CONFIG_PATH, 'r') as f:
        lines = f.readlines()
    return [line.split()[1] for line in lines if line.startswith('Host ')]

def remove_config() -> None:
    """Remove an SSH config entry interactively."""
    hosts = get_hosts()
    
    if not hosts:
        print(Fore.YELLOW + "No SSH configurations found." + ColoramaStyle.RESET_ALL)
        return

    result = radiolist_dialog(
        title="Remove SSH Config",
        text="Select a host to remove:",
        values=[(host, host) for host in hosts],
        style=Style.from_dict({
            'dialog': 'bg:#880000',
            'dialog frame.label': 'bg:#ffffff #000000',
            'dialog.body': 'bg:#000000 #ff0000',
            'dialog shadow': 'bg:#440000',
        })
    ).run()

    if result is None:
        print(Fore.YELLOW + "Operation cancelled." + ColoramaStyle.RESET_ALL)
        return

    host_to_remove = result

    confirm = prompt(f"Are you sure you want to remove the config for {host_to_remove}? (yes/no): ").lower()

    if confirm != "yes":
        print(Fore.YELLOW + "Operation cancelled." + ColoramaStyle.RESET_ALL)
        return

    with open(SSH_CONFIG_PATH, 'r') as f:
        lines = f.readlines()

    new_lines = []
    skip = False
    for line in lines:
        if line.startswith(f"Host {host_to_remove}"):
            skip = True
        elif line.startswith("Host "):
            skip = False
        if not skip:
            new_lines.append(line)

    if len(new_lines) < len(lines):
        backup_ssh_config()
        
        with open(SSH_CONFIG_PATH, 'w') as f:
            f.writelines(new_lines)
        
        print(Fore.GREEN + f"Removed SSH config for host {host_to_remove}" + ColoramaStyle.RESET_ALL)
    else:
        print(Fore.YELLOW + f"No changes made. Host {host_to_remove} not found in config." + ColoramaStyle.RESET_ALL)

def restore_config() -> None:
    """Restore a previous SSH config backup interactively."""
    backups = sorted(BACKUP_DIR.glob("config_*.bak"), reverse=True)
    if not backups:
        print(Fore.YELLOW + "No backups found." + ColoramaStyle.RESET_ALL)
        return

    result = radiolist_dialog(
        title="Restore SSH Config",
        text="Select a backup to restore:",
        values=[(str(backup), backup.name) for backup in backups],
        style=dialog_style
    ).run()

    if result is None:
        print(Fore.YELLOW + "Operation cancelled." + ColoramaStyle.RESET_ALL)
        return

    backup_to_restore = Path(result)

    confirm = prompt(f"Are you sure you want to restore the backup {backup_to_restore.name}? (yes/no): ").lower()

    if confirm != "yes":
        print(Fore.YELLOW + "Operation cancelled." + ColoramaStyle.RESET_ALL)
        return

    import shutil
    shutil.copy(backup_to_restore, SSH_CONFIG_PATH)
    print(Fore.GREEN + f"Restored {backup_to_restore.name} to {SSH_CONFIG_PATH}" + ColoramaStyle.RESET_ALL)

def main() -> None:
    """Main function to handle command-line arguments and execute corresponding actions."""
    parser = argparse.ArgumentParser(description="SSH Config Manager")
    parser.add_argument("action", choices=["add", "list", "remove", "backup", "restore"], help="Action to perform")
    args = parser.parse_args()

    if args.action == "add":
        add_config()
    elif args.action == "list":
        list_configs()
    elif args.action == "remove":
        remove_config()
    elif args.action == "backup":
        backup_path = backup_ssh_config()
        print(Fore.GREEN + f"Backup created: {backup_path}" + ColoramaStyle.RESET_ALL)
    elif args.action == "restore":
        restore_config()

if __name__ == "__main__":
    main()