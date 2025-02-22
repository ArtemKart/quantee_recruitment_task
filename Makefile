EDITABLE ?= no
APP_NAME ?= app

ifeq ($(OS),Windows_NT)
    VENV_ACTIVATE := .venv\Scripts\activate
else
    VENV_ACTIVATE := .venv/bin/activate
endif

ifeq ($(EDITABLE), yes)
	PIP_INSTALL := pip install -U -e .[dev]
else
	PIP_INSTALL := pip install -U .[dev]
endif

.PHONY: install lint

$(VENV_ACTIVATE): pyproject.toml .pre-commit-config.yaml
	python3.12 -m venv .venv
	. $(VENV_ACTIVATE) && pip install --upgrade pip \
		&& $(PIP_INSTALL)
	. $(VENV_ACTIVATE) && pre-commit install

install: $(VENV_ACTIVATE)

lint: install
	. $(VENV_ACTIVATE) && black . && pylama $(APP_NAME) -l mccabe,pycodestyle,pyflakes,radon,mypy --async
