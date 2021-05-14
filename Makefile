PYTHON ?= python39
ARGSTR ?= --argstr python $(PYTHON)

CACHIX_CACHE ?= datakurre

TEST = $(wildcard tests/*.py)
SRC = $(wildcard src/sphinxcontrib/httpexample/*.py)

.PHONY: all
all: test coverage

.PHONY: nix-%
nix-%: requirements.nix
	nix-shell setup.nix $(ARGSTR) -A package --run "$(MAKE) $*"

nix-env: requirements.nix
	nix-build setup.nix $(ARGSTR) -A env

nix-shell: requirements.nix
	nix-shell setup.nix $(ARGSTR) -A package

.PHONY: cache
cache:
	nix-store --query --references $$(nix-instantiate shell.nix --argstr python $(PYTHON)) --references $$(nix-instantiate default.nix --argstr python $(PYTHON)) | \
	xargs nix-store --realise | xargs nix-store --query --requisites | cachix push $(CACHIX_CACHE)

.PHONY: docs
docs: requirements.nix
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

.PHONY: test
test:
	flake8 src
	py.test

.PHONY: push-cachix
push-cachix:
	nix-build setup.nix --argstr python python3 -A env|cachix push datakurre
	nix-build setup.nix --argstr python python2 -A env|cachix push datakurre

.PHONY: freeze
freeze:
	@grep "name" requirements.nix |grep -Eo "\"(.*)\""|grep -Eo "[^\"]+"|sed -r "s|-([0-9\.]+)|==\1|g"

###

.cache:
	mkdir -p .cache
	if [ -d ~/.cache/pip ]; then ln -s ~/.cache/pip ./.cache; fi

.coverage: $(TEST) $(SRC)
	coverage run setup.py test

.PHONY: requirements
requirements: .cache requirements-$(PYTHON).nix

requirements-$(PYTHON).nix: .cache requirements-$(PYTHON).txt
	pip2nix generate -r requirements-$(PYTHON).txt --output=requirements-$(PYTHON).nix

requirements-$(PYTHON).txt: .cache requirements.txt
	pip2nix generate -r requirements.txt --output=requirements-$(PYTHON).nix
	@grep "pname =\|version =" requirements-$(PYTHON).nix|awk "ORS=NR%2?FS:RS"|sed 's|.*"\(.*\)";.*version = "\(.*\)".*|\1==\2|' > requirements-$(PYTHON).txt
