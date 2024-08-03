PYTHON ?= python39
FEATURE ?=
ARGSTR ?= --argstr python $(PYTHON) --argstr feature "$(FEATURE)"

CACHIX_CACHE ?= datakurre

TEST = $(wildcard tests/*.py)
SRC = $(wildcard src/sphinxcontrib/httpexample/*.py)

# Sphinx variables
# You can set these variables from the command line.
SPHINXOPTS      ?=
# Internal variables.
SPHINXBUILD     = "$(realpath env/bin/sphinx-build)"
SPHINXAUTOBUILD = "$(realpath env/bin/sphinx-autobuild)"
DOCS_DIR        = ./docs/
BUILDDIR        = ../_build/
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) .

.PHONY: all
all: test coverage

.PHONY: nix-%
nix-%:
	nix-shell setup.nix $(ARGSTR) -A package --run "$(MAKE) $*"

nix-env:
	nix-build setup.nix $(ARGSTR) -A env

nix-shell:
	nix-shell setup.nix $(ARGSTR) -A package

.PHONY: cache
cache:
	nix-store --query --references $$(nix-instantiate default.nix --argstr python $(PYTHON)) | \
	xargs nix-store --realise | xargs nix-store --query --requisites | cachix push $(CACHIX_CACHE)

.PHONY: docs
docs:
	cd $(DOCS_DIR) && $(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

.PHONY: livehtml
livehtml:  ## Rebuild Sphinx documentation on changes, with live-reload in the browser
	cd "$(DOCS_DIR)" && ${SPHINXAUTOBUILD} \
		--ignore "*.swp" \
		--port 8050 \
		-b html . "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

.PHONY: coverage
coverage: .coverage
	coverage report --fail-under=80

.PHONY: coveralls
coveralls: .coverage
	coveralls --service=github

.PHONY: show
show:
	pip list

.PHONY: test
test:
	flake8 src
	py.test

###

.cache:
	mkdir -p .cache
	if [ -d ~/.cache/pip ]; then ln -s ~/.cache/pip ./.cache; fi

.coverage: $(TEST) $(SRC)
	coverage run setup.py test

.PHONY: requirements
requirements: .cache nix/requirements-$(PYTHON).nix

nix/requirements-$(PYTHON).nix: .cache requirements-$(PYTHON).txt
	nix-shell -p "(import ./nix {}).pip2nix.$(PYTHON)" --run "pip2nix generate -r requirements-$(PYTHON).txt --output=nix/requirements-$(PYTHON).nix"

requirements-$(PYTHON).txt: .cache requirements.txt
	nix-shell -p "(import ./nix {}).pip2nix.$(PYTHON)" --run "pip2nix generate -r requirements.txt --output=nix/requirements-$(PYTHON).nix"
	@grep "pname =\|version =" nix/requirements-$(PYTHON).nix|awk "ORS=NR%2?FS:RS"|sed 's|.*"\(.*\)";.*version = "\(.*\)".*|\1==\2|' > requirements-$(PYTHON).txt
