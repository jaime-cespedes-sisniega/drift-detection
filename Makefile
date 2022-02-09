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
	mkdir .multiproc
	export PROMETHEUS_MULTIPROC_DIR="${CURDIR}/.multiproc/"
	uvicorn app.main:app --host 0.0.0.0 --port 5001 --workers 5

serve-prod:
	mkdir .multiproc
	export PROMETHEUS_MULTIPROC_DIR="${CURDIR}/.multiproc/"
	gunicorn -b 0.0.0.0:5001 -w 5 -t 120 -c gunicorn_conf.py -k uvicorn.workers.UvicornWorker app.main:app

build:
	docker build -t drift-detection .

run:
	docker run -d --name drift-detection -p 5001:5001 -e NUM_WORKERS=5 -e TIMEOUT=120 \
    drift-detection
