PYTHON ?= python3
ARGSTR ?= --argstr python $(PYTHON)

TEST = $(wildcard tests/*.py)
SRC = $(wildcard src/sphinxcontrib/httpexample/*.py)

.PHONY: all
all: test coverage

.PHONY: nix-%
nix-%: requirements.nix
	nix-shell setup.nix $(ARGSTR) -A develop --run "$(MAKE) $*"

nix-env: requirements.nix
	nix-build setup.nix $(ARGSTR) -A env

nix-shell: requirements.nix
	nix-shell setup.nix $(ARGSTR) -A develop

.PHONY: docs
docs: requirements.nix
	nix-build release.nix $(ARGSTR) -A docs

.PHONY: coverage
coverage: .coverage
	coverage report --fail-under=80

.PHONY: coveralls
coveralls: .coverage
	coveralls

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

.coverage: $(TEST) $(SRC)
	coverage run setup.py test

requirements.nix: requirements.txt
	nix-shell setup.nix -A pip2nix \
	  --run "pip2nix generate -r requirements.txt --output=requirements.nix"
