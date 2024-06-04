PY?=python3

BASEDIR=$(CURDIR)
VENV=$(BASEDIR)/.venv
BIN=$(VENV)/bin
PYTHON=$(BIN)/python
TESTSDIR=$(BASEDIR)/.tests
SCHEMASDIR=$(BASEDIR)/.schemas
export PYTHONPATH := $(BASEDIR):$(TESTSDIR)

VERBOSE ?= 1

help:
	@echo 'Makefile for a testing pyvideo/data                                 '
	@echo '                                                                   '
	@echo 'Usage:                                                             '
	@echo '   make test                   run all tests                       '
	@echo '   make test-schemas           run schema validation tests         '
	@echo '   make test-ids-unique        run "unique IDs" test               '
	@echo '   make test-slugs-unique      run "unique slugs" test             '
	@echo '   make test-render-rest       run ReST rendering test             '
	@echo '                                                                   '
	@echo 'Set the VERBOSE variable to 1 to enable more verbose output.       '
	@echo 'e.g. make VERBOSE=1 test                                           '
	@echo '                                                                   '

.venv:
	python3 -m venv $(VENV)

install-deps: .venv
	$(BIN)/pip install -r $(TESTSDIR)/requirements.txt

test-schemas: install-deps
	$(PYTHON) $(TESTSDIR)/schemas.py -d $(BASEDIR) -s $(SCHEMASDIR) -v $(VERBOSE)

test-ids-unique: install-deps
	$(PYTHON) $(TESTSDIR)/ids_unique.py -d $(BASEDIR) -v $(VERBOSE)

test-slugs-unique: install-deps
	$(PYTHON) $(TESTSDIR)/slugs_unique.py -d $(BASEDIR) -v $(VERBOSE)

test-render-rest: install-deps
	$(PYTHON) $(TESTSDIR)/render_rest.py -d $(BASEDIR) -v $(VERBOSE)

test-shape: install-deps
	$(PYTHON) $(TESTSDIR)/shape.py -d $(BASEDIR) -v $(VERBOSE)

test-languages: install-deps
	$(PYTHON) $(TESTSDIR)/languages.py -d $(BASEDIR) -v $(VERBOSE)

test-filename-length: install-deps
	$(PYTHON) $(TESTSDIR)/filename_length.py -d $(BASEDIR) -v $(VERBOSE)

test: test-schemas test-ids-unique test-slugs-unique test-render-rest test-languages test-filename-length

.PHONY: help test test-schemas test-ids-unique test-slugs-unique test-render-rest test-shape test-languages
