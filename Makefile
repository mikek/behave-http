# Adopted from https://github.com/audreyr/cookiecutter-pypackage

TEST_SERVER ?= "http://127.0.0.1:55080"

.PHONY: clean-pyc clean-build clean

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean - two above and coverage reports"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
#	@echo "test-all - run tests on every Python version with tox"
	@echo "test-coverage - check code coverage while running tests with the default Python"
	@echo "coverage - run 'test-coverage', show report and generate html"
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

check-testserver:
	curl -w "Response code: %{http_code}\n" $(TEST_SERVER)/behave-http

#test-all:
#	tox

test: check-testserver
	python setup.py behave_test -q --format progress3

# These coverage rules can be optimized not to rerun if deps were not changed,
# but that is an overkill for such a tiny test suite.
test-coverage: check-testserver
	# We really need a full path to 'behave' for coverage.py to work
	$(eval BEHAVE := $(shell which behave))
	COVERAGE_PROCESS_START="yep" coverage run --branch --source='behave_http' $(BEHAVE) -q -f progress3

coverage-report: test-coverage
	coverage report -m

coverage-html: test-coverage
	coverage html
#	open htmlcov/index.html

coverage: coverage-html coverage-report

%.html: %.md
	markdown $^ > $@

docs: README.html

release: lint test clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
