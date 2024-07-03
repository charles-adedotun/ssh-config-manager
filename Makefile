# ssh-config-manager/Makefile

.PHONY: all install uninstall clean test add list remove backup restore help

SCRIPT_NAME = ssh_config_manager.py
INSTALL_DIR = /usr/local/bin
VENV_DIR = venv

# ANSI color codes
GREEN = \033[0;32m
YELLOW = \033[1;33m
CYAN = \033[0;36m
RED = \033[0;31m
NC = \033[0m # No Color

all: help

venv: requirements.txt
	@python3 -m venv $(VENV_DIR)
	@./$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "$(GREEN)Virtual environment created and dependencies installed.$(NC)"

install: venv
	@echo "$(YELLOW)Installing $(SCRIPT_NAME) to $(INSTALL_DIR)$(NC)"
	@sudo cp $(SCRIPT_NAME) $(INSTALL_DIR)/$(SCRIPT_NAME)
	@sudo chmod +x $(INSTALL_DIR)/$(SCRIPT_NAME)
	@echo "$(GREEN)Installation complete. You can now use 'make' commands to manage SSH configs.$(NC)"
	@echo "\n$(CYAN)Available commands:$(NC)"
	@$(MAKE) --no-print-directory help

uninstall:
	@echo "$(YELLOW)Uninstalling $(SCRIPT_NAME) from $(INSTALL_DIR)$(NC)"
	@sudo rm -f $(INSTALL_DIR)/$(SCRIPT_NAME)
	@echo "$(GREEN)Uninstallation complete.$(NC)"

clean:
	@echo "$(YELLOW)Cleaning up...$(NC)"
	@rm -rf $(VENV_DIR)
	@rm -f *~
	@echo "$(GREEN)Cleanup complete.$(NC)"

test: venv
	@echo "$(YELLOW)Running tests...$(NC)"
	@./$(VENV_DIR)/bin/pytest tests/
	@echo "$(GREEN)Tests completed.$(NC)"

add:
	@echo "$(CYAN)Adding new SSH config entry...$(NC)"
	@./$(VENV_DIR)/bin/python $(SCRIPT_NAME) add

list:
	@echo "$(CYAN)Listing SSH config entries...$(NC)"
	@./$(VENV_DIR)/bin/python $(SCRIPT_NAME) list

remove:
	@echo "$(CYAN)Removing SSH config entry...$(NC)"
	@./$(VENV_DIR)/bin/python $(SCRIPT_NAME) remove

backup:
	@echo "$(CYAN)Creating backup of SSH config...$(NC)"
	@./$(VENV_DIR)/bin/python $(SCRIPT_NAME) backup

restore:
	@echo "$(CYAN)Restoring SSH config from backup...$(NC)"
	@./$(VENV_DIR)/bin/python $(SCRIPT_NAME) restore

help:
	@echo "  $(GREEN)make install$(NC)    - Install the SSH config manager"
	@echo "  $(RED)make uninstall$(NC)  - Uninstall the SSH config manager"
	@echo "  $(GREEN)make add$(NC)        - Add a new SSH config entry"
	@echo "  $(GREEN)make list$(NC)       - List all SSH config entries"
	@echo "  $(YELLOW)make remove$(NC)     - Remove an SSH config entry"
	@echo "  $(GREEN)make backup$(NC)     - Backup the current SSH config"
	@echo "  $(YELLOW)make restore$(NC)    - Restore a previous SSH config backup"
	@echo "  $(RED)make clean$(NC)      - Clean up temporary files"
	@echo "  $(CYAN)make test$(NC)       - Run tests"
	@echo "  $(CYAN)make help$(NC)       - Show this help message"