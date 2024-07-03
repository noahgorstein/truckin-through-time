SHELL = /bin/bash -c
VIRTUAL_ENV = $(PWD)/venv
export BASH_ENV=$(VIRTUAL_ENV)/bin/activate
PYTHON_SOURCE = scraper

.PHONY: clean format
default: help

clean: ## Delete database
	rm database.db

format: ## Run formatters (black, isort)
	black $(PYTHON_SOURCE) && isort $(PYTHON_SOURCE)

lint: ## Lint python
	mypy $(PYTHON_SOURCE) && flake8 $(PYTHON_SOURCE)

.SILENT: help
#% Available Commands:
help: ## List available commands 
	grep '^#%' $(MAKEFILE_LIST) | sed -e 's/#%//'
	grep '^[a-zA-Z]' $(MAKEFILE_LIST) | awk -F ':.*?## ' 'NF==2 {printf "   %-20s%s\n", $$1, $$2}' | sort
