# Makefile for Sphinx documentation
.DEFAULT_GOAL   = help
SHELL           = bash

# You can set these variables from the command line.
SPHINXOPTS      ?=
PAPER           ?=

# Internal variables.
MAKEFILE_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
ifdef IN_NIX_SHELL
BIN_FOLDER      = $(shell dirname "$$(command -v python)")
VENV_FOLDER     = $(shell dirname "$(BIN_FOLDER)")
else
VENV_FOLDER     = $(MAKEFILE_DIR)/.venv
BIN_FOLDER      = $(VENV_FOLDER)/bin
endif
DOCS_DIR        = $(MAKEFILE_DIR)/docs/
BUILDDIR        = $(MAKEFILE_DIR)/_build
SPHINXBUILD     = "$(realpath $(BIN_FOLDER)/sphinx-build)"
SPHINXAUTOBUILD = "$(realpath $(BIN_FOLDER)/sphinx-autobuild)"
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
PYTHONVERSION   = >=3.11,<3.15

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help:  ## This help message
	@grep -Eh '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' | uniq

SPHINX ?= 8.3.2
PYTHON ?= python313

# docs contains example of custom http-example builder module
export PYTHONPATH=$(DOCS_DIR)

# environment management
.PHONY: dev
dev:  ## Install required Python, create Python virtual environment, and install package requirements
ifndef IN_NIX_SHELL
	@uv python install "$(PYTHONVERSION)"
	@uv venv --python "$(PYTHONVERSION)"
	@uv sync
endif

.PHONY: sync
sync:  ## Sync package requirements
ifndef IN_NIX_SHELL
	@uv sync
endif

.PHONY: init
init: clean clean-python dev  ## Clean docs build directory and initialize Python virtual environment

.PHONY: clean
clean:  ## Clean docs build directory
	cd $(DOCS_DIR) && rm -rf $(BUILDDIR)/

.PHONY: clean-python
clean-python: clean
	rm -rf .venv/
# /environment management


# documentation builders
.PHONY: html
html: dev  ## Build html
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

.PHONY: livehtml
livehtml: dev  ## Rebuild Sphinx documentation on changes, with live-reload in the browser
	cd "$(DOCS_DIR)" && ${SPHINXAUTOBUILD} \
		--ignore "*.swp" \
		--port 8050 \
		-b html . "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
# /documentation builders


# development and contributing
.PHONY: format
format:  ## Format code
	treefmt

.PHONY: show
show:  ## Show installed packages
	@python --version
	@python -c "from importlib import metadata; print('\n'.join(sorted(d.metadata['Name'] + f' {d.version}' for d in metadata.distributions() if d.metadata['Name'].lower() in ['docutils', 'sphinx'])))"

.PHONY: test
test: ## Run tests
	$(BIN_FOLDER)/pytest --cov sphinxcontrib.httpexample tests

.PHONY: devenv-%
devenv-%: devenv.local.nix
	devenv shell $(MAKE) $*

shell: devenv.local.nix  ## Start a shell with the development environment
	devenv shell

htmlcov: .coverage
	coverage html

coverage.xml: .coverage
	coverage xml

coverage: coverage.xml

.PHONY: test\ all
test\ all:  ## Test all supported versions
	make PYTHON=python314 SPHINX=8.2.3 clean devenv-show devenv-test
	make PYTHON=python314 SPHINX=8.1.3 clean devenv-show devenv-test
	make PYTHON=python314 SPHINX=8.0.2 clean devenv-show devenv-test
	make PYTHON=python314 SPHINX=7.4.7 clean devenv-show devenv-test
	make PYTHON=python313 SPHINX=8.2.3 clean devenv-show devenv-test
	make PYTHON=python313 SPHINX=8.1.3 clean devenv-show devenv-test
	make PYTHON=python313 SPHINX=8.0.2 clean devenv-show devenv-test
	make PYTHON=python313 SPHINX=7.4.7 clean devenv-show devenv-test
	make PYTHON=python312 SPHINX=8.2.3 clean devenv-show devenv-test
	make PYTHON=python312 SPHINX=8.1.3 clean devenv-show devenv-test
	make PYTHON=python312 SPHINX=8.0.2 clean devenv-show devenv-test
	make PYTHON=python312 SPHINX=7.4.7 clean devenv-show devenv-test
	make PYTHON=python311 SPHINX=8.2.3 clean devenv-show devenv-test
	make PYTHON=python311 SPHINX=8.1.3 clean devenv-show devenv-test
	make PYTHON=python311 SPHINX=8.0.2 clean devenv-show devenv-test
	make PYTHON=python311 SPHINX=7.4.7 clean devenv-show devenv-test
	make PYTHON=python310 SPHINX=8.1.3 clean devenv-show devenv-test
	make PYTHON=python310 SPHINX=8.0.2 clean devenv-show devenv-test
	make PYTHON=python310 SPHINX=7.4.7 clean devenv-show devenv-test

devenv.local.nix:
	@echo '{ pkgs, ...}: { languages.python = { interpreter = pkgs.$(PYTHON); dependencies = [ "sphinx$(subst .,,$(SPHINX))" "dev" ]; }; }' > devenv.local.nix
# /development and contributing
