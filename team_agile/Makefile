include .env

# ***************************************
# POETRY COMMANDS
# ***************************************
.PHONY: format
pall: poetry run black .

.PHONY: run
run:
	poetry run uvicorn main:app --reload --port $(PORT)

.PHONY: all
all: pcheck

.PHONY: check
check: flake8 isort pycodestyle

.PHONY: flake8
flake8:
	poetry run flake8 --exclude=.venv,venv,.git,__pycache__  .

.PHONY: isort
isort:
	poetry run isort --check-only .

.PHONY: sort
sort:
	poetry run isort .

.PHONY: pycodestyle
pycodestyle:
	poetry run pycodestyle --exclude=.venv,venv,.git,__pycache__ .

.PHONY: test
test: 
	poetry run pytest tests/

.PHONY: script
script:
	python -m scripts.load_data