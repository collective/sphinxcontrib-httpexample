SYSTEM ?= x86_64-linux
PYTHON ?= python3

TEST = $(wildcard tests/*.py)
SRC = $(wildcard src/sphinxcontrib/httpexample/*.py)

all: test

buildEnv: result/bin/$(PYTHON)

coverage: .coverage
	nix-shell --run "coverage report --fail-under=80"

dist:
	nix-build release.nix -A tarball

docs: result/sphinxcontrib-httpexample.pdf

shell:
	nix-shell --arg "pkgs" "import <nixpkgs> {}" \
	          --arg "pythonPackages" "(import <nixpkgs> {}).$(PYTHON)Packages"

test:
	nix-build release.nix -A build.$(SYSTEM).$(PYTHON)
	nix-shell --run "bin/code-analysis"

.PHONY: all buildEnv coverage dist docs shell test

###

.coverage: $(TEST) $(SRC)
	nix-shell --run "coverage run setup.py test"

result/bin/$(PYTHON):
	nix-build release.nix -A buildEnv.$(SYSTEM).$(PYTHON)

result/sphinxcontrib-httpexample.pdf:
	nix-build release.nix -A docs
