GLOBAL_PY := python3.8
SERVE_VENV ?= .serve_venv
SERVE_PY := $(SERVE_VENV)/bin/python

.PHONY: init-serve-env
init-serve-env:
	$(GLOBAL_PY) -m venv $(SERVE_VENV)
	$(SERVE_PY) -m pip install wheel gunicorn -r requirements.txt


.PHONY: update-requirements
update-requirements:
	pipenv lock -r > requirements.txt
