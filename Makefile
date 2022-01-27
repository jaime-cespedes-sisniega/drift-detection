.ONESHELL:
SHELL := /bin/bash

VENV=.venv

install:
	python3 -m venv $(VENV)
	source $(VENV)/bin/activate
	pip3 install --upgrade pip &&\
				 pip3 install -r requirements/requirements.txt \
				              -r requirements/tox_requirements.txt

tox:
	$(VENV)/bin/tox

serve-dev:
	uvicorn app.main:app --host 0.0.0.0 --port 5001 --workers 1