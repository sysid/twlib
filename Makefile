.DEFAULT_GOAL := help
MAKEFLAGS += --no-print-directory

# You can set these variables from the command line, and also from the environment for the first two.
SOURCEDIR     = source
BUILDDIR      = build
MAKE          = make
VERSION       = $(shell cat VERSION)

app_root = $(PROJ_DIR)
app_root ?= .
pkg_src =  $(app_root)/src/twlib
tests_src = $(app_root)/tests

################################################################################
# Developing \
DEVELOP: ## ############################################################

.PHONY: test-proj-xxx
test-proj-xxx:  ## test-proj-xxx: create ~/xxx/test_proj to test installed confguard
	rm -fr ~/xxx/test_proj
	rm -fr /tmp/confguard
	cp -a tests/resources/ref_proj ~/xxx/test_proj

.PHONY: links
links:  test-proj-xxx ## links
	pushd ~/xxx/test_proj && CONFGUARD_PATH=/tmp/confguard confguard -v guard .

.PHONY: view-links
view-links:  ## view-links
	find tests/resources/*_proj -ls

################################################################################
# Building, Deploying \
BUILDING:  ## ############################################################

.PHONY: build
build: clean style  ## format and build
	@echo "building"
	python -m build

.PHONY: dist
dist:  ## - create a wheel distribution package
	@python setup.py bdist_wheel


.PHONY: dist-test
dist-test: dist  ## - test a wheel distribution package
	@cd dist && ../tests/test-dist.bash ./twlib-*-py3-none-any.whl

.PHONY: upload
upload:   ## twine upload
	@echo "upload"
	twine upload --verbose dist/*

.PHONY: install
install: uninstall  ## pipx install
	pipx install .

.PHONY: uninstall
uninstall:  ## pipx uninstall
	-pipx uninstall twlib

.PHONY: bump-major
bump-major:  ## bump-major, tag and push
	bumpversion --commit --tag major
	git push --tags

.PHONY: bump-minor
bump-minor:  ## bump-minor, tag and push
	bumpversion --commit --tag minor
	git push --tags

.PHONY: bump-patch
bump-patch:  ## bump-patch, tag and push
	bumpversion --commit --tag patch
	git push --tags

.PHONY: docu-twlib
docu-twlib:  ## docu-twlib: copy to clipboard for usage in README
	python -m twlib --help| pbcopy

.PHONY: docu-opengit
docu-opengit:  ## docu-opengit: copy to clipboard for usage in README
	git-open --help| pbcopy
################################################################################
# Testing \
TESTING:  ## ############################################################

.PHONY: tox
tox:   ## Run tox
	$(tox)


.PHONY: test
test:  ## - run tests
	#@python -m pytest tests/
	python -m pytest -ra --junitxml=report.xml --cov-config=setup.cfg --cov-report=xml --cov-report term --cov=$(pkg_src) -vv tests/


.PHONY: coverage
coverage:  ## - perform test coverage checks
	python -m coverage erase
	python -m coverage run --include=$(pkg_src)/* -m pytest -ra
	#python -m coverage report -m
	python -m coverage html
	open htmlcov/index.html  # work on macOS

################################################################################
# Code Quality \
QUALITY:  ## ############################################################

.PHONY: format
format:  ## - perform code style format
	@black src tests


.PHONY: check-format
check-format:  ## - check code format compliance
	@black --check twlib tests


.PHONY: sort-imports
sort-imports:  ## - apply import sort ordering
	@isort src --profile black


.PHONY: check-sort-imports
check-sort-imports:  ## - check imports are sorted
	@isort . --check-only --profile black


.PHONY: style
style: sort-imports format  ## - perform code style format


.PHONY: check-style
check-style: check-sort-imports check-format  ## - check code style compliance


.PHONY: check-types
check-types:  ## - check type hint annotations
	@mypy -p twlib --ignore-missing-imports


.PHONY: check-lint
check-lint:  ## - run static analysis checks
	@pylint --rcfile=.pylintrc twlib ./tests setup.py ./examples


.PHONY: check-static-analysis
check-static-analysis: check-lint check-types  ## - check code style compliance


################################################################################
# Clean \
CLEAN:  ## ############################################################

.PHONY: clean
clean: clean-build clean-pyc  ## remove all build, test, coverage and Python artifacts

.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg-info' -exec rm -fr {} +
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


################################################################################
# Misc \
MISC:  ## ############################################################
define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z0-9_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("\033[36m%-20s\033[0m %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

.PHONY: help
help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)
