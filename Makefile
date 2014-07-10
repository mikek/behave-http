# Adopted from https://github.com/audreyr/cookiecutter-pypackage

TEST_SERVER ?= "http://127.0.0.1:55080"
BEHAVE := $(shell which behave)

.PHONY: clean-pyc clean-build clean

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean - two above and coverage reports"
	@echo "lint - check style with flake8"
#	@echo "test - run tests quickly with the default Python"
#	@echo "test-all - run tests on every Python version with tox"
	@echo "behave-test - run feature tests with the default Python"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate README.HTML from README.md"
	@echo "release - package and upload a release"
	@echo "dist - package"

clean: clean-build clean-pyc
	rm -fr htmlcov/
	rm -f .coverage

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -rf eggs

clean-pyc:
	find . -name __pycache__ -type d -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 behave_http features setup.py testserver.py

behave-test:
	test `curl -s -w %{http_code} $(TEST_SERVER)/behave-http` -eq 200
	python setup.py behave_test

#test-all:
#	tox

coverage:
	COVERAGE_PROCESS_START="yep" coverage run --source='behave_http' $(BEHAVE) -q -f progress
	coverage report -m
	coverage html
#	open htmlcov/index.html

%.html: %.md
	markdown $^ > $@

docs: README.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
