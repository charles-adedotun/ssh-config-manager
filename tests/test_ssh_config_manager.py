# tests/test_ssh_config_manager.py

import pytest
import os
from pathlib import Path
import sys
import io
from unittest.mock import patch, MagicMock

# Add the parent directory to the Python path so we can import the main script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ssh_config_manager

@pytest.fixture
def temp_ssh_config(tmp_path):
    config_content = """
Host example1
    HostName example1.com
    User user1
    IdentityFile ~/.ssh/id_rsa

Host example2
    HostName example2.com
    User user2
    IdentityFile ~/.ssh/id_rsa_example2
"""
    config_file = tmp_path / "config"
    config_file.write_text(config_content)
    return config_file

@pytest.fixture
def mock_ssh_config_path(monkeypatch, temp_ssh_config):
    monkeypatch.setattr(ssh_config_manager, "SSH_CONFIG_PATH", temp_ssh_config)
    return temp_ssh_config

@pytest.fixture
def mock_backup_dir(tmp_path):
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()
    return backup_dir

@pytest.fixture
def mock_all_paths(monkeypatch, temp_ssh_config, mock_backup_dir):
    monkeypatch.setattr(ssh_config_manager, "SSH_CONFIG_PATH", temp_ssh_config)
    monkeypatch.setattr(ssh_config_manager, "BACKUP_DIR", mock_backup_dir)
    monkeypatch.setattr(ssh_config_manager, "CONFIG_DIR", mock_backup_dir.parent)

def test_load_config(mock_ssh_config_path):
    config = ssh_config_manager.load_config()
    assert isinstance(config, dict)

def test_update_ssh_config(mock_ssh_config_path):
    ssh_config_manager.update_ssh_config("newhost", {
        "HostName": "newhost.com",
        "User": "newuser",
        "IdentityFile": "~/.ssh/id_rsa_new"
    })
    with open(mock_ssh_config_path, "r") as f:
        content = f.read()
    assert "Host newhost" in content
    assert "HostName newhost.com" in content
    assert "User newuser" in content
    assert "IdentityFile ~/.ssh/id_rsa_new" in content

def test_remove_config(mock_all_paths):
    mock_dialog = MagicMock()
    mock_dialog.run.return_value = "example1"
    with patch('ssh_config_manager.radiolist_dialog', return_value=mock_dialog), \
         patch('ssh_config_manager.prompt', return_value="yes"):
        ssh_config_manager.remove_config()

    with open(ssh_config_manager.SSH_CONFIG_PATH, "r") as f:
        content = f.read()
    assert "Host example1" not in content
    assert "Host example2" in content

def test_list_configs(mock_ssh_config_path, capsys):
    ssh_config_manager.list_configs()
    captured = capsys.readouterr()
    assert "Host example1" in captured.out
    assert "Host example2" in captured.out

def test_add_config(mock_all_paths):
    with patch('ssh_config_manager.prompt', side_effect=["testhost", "testhost.com", "testuser", "~/.ssh/id_rsa_test"]):
        ssh_config_manager.add_config()

    with open(ssh_config_manager.SSH_CONFIG_PATH, "r") as f:
        content = f.read()
    assert "Host testhost" in content
    assert "HostName testhost.com" in content
    assert "User testuser" in content
    assert "IdentityFile ~/.ssh/id_rsa_test" in content

def test_backup_ssh_config(mock_all_paths):
    backup_path = ssh_config_manager.backup_ssh_config()
    assert backup_path.exists()
    assert backup_path.parent == ssh_config_manager.BACKUP_DIR

def test_restore_config(mock_all_paths):
    # First, create a backup
    backup_path = ssh_config_manager.backup_ssh_config()
    
    # Modify the current config
    ssh_config_manager.update_ssh_config("newhost", {
        "HostName": "newhost.com",
        "User": "newuser",
        "IdentityFile": "~/.ssh/id_rsa_new"
    })
    
    # Now restore
    mock_dialog = MagicMock()
    mock_dialog.run.return_value = str(backup_path)
    with patch('ssh_config_manager.radiolist_dialog', return_value=mock_dialog), \
         patch('ssh_config_manager.prompt', return_value="yes"):
        ssh_config_manager.restore_config()

    with open(ssh_config_manager.SSH_CONFIG_PATH, "r") as f:
        content = f.read()
    assert "Host newhost" not in content
    assert "Host example1" in content
    assert "Host example2" in content

def test_main(mock_all_paths):
    test_args = ['ssh_config_manager.py', 'list']
    with patch.object(sys, 'argv', test_args):
        with patch('builtins.print') as mock_print:
            ssh_config_manager.main()
            mock_print.assert_called()

if __name__ == "__main__":
    pytest.main(["-v", __file__])