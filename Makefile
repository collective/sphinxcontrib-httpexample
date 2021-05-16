PYTHON ?= python39
ARGSTR ?= --argstr python $(PYTHON)

CACHIX_CACHE ?= datakurre

TEST = $(wildcard tests/*.py)
SRC = $(wildcard src/sphinxcontrib/httpexample/*.py)

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
	sphinx-build -b html docs docs/html
ifeq "$(PYTHON)" "python27"
	sphinx-build -b pdf docs docs/pdf
endif

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
