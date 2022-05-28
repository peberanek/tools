# Inspired by https://github.com/trezor/trezor-firmware/blob/master/Makefile

#
## help commands:
#

.PHONY: help
help: ## show this help and exit
	@awk -f ./help.awk $(MAKEFILE_LIST)


#
## style commands:
#

PY_FILES = $(shell find . -type f -name '*.py' | sed 'sO^\./OO' | grep -f ./style.py.patterns_include | grep -v -f ./style.py.patterns_exclude )
PY_FILES += $(shell cat ./style.py.files_include )

.PHONY: style_check
style_check: pystyle_check ## run all code style checks

.PHONY: pystyle_check
pystyle_check: ## run Python code style check
	black --version
	isort --version-number
	@echo [BLACK]
	@black --check $(PY_FILES)
	@echo [ISORT]
	@isort --profile black --check-only $(PY_FILES)

.PHONY: style
style: pystyle ## run all code formatters

.PHONY: pystyle
pystyle: ## run Python code formatters
	black --version
	isort --version-number
	@echo [BLACK]
	@black $(PY_FILES)
	@echo [ISORT]
	@isort --profile black $(PY_FILES)


#
## misc commands:
#

.PHONY: venv
venv: VENV_DIR = venv
venv: ## create Python virtual environment
	python3 -m venv --clear --upgrade-deps $(VENV_DIR)
	source $(VENV_DIR)/bin/activate && python3 -m pip install -r venv_requirements.txt

.PHONY: show_py_files
show_py_files:
	@echo $(PY_FILES)