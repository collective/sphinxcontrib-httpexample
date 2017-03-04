SYSTEM ?= x86_64-linux
PYTHON ?= python3

TEST = $(wildcard tests/*.py)
SRC = $(wildcard src/sphinxcontrib/httpexample/*.py)

all: test

buildEnv: result/bin/$(PYTHON)

docs: result/sphinxcontrib-httpexample.pdf

dist:
	nix-build release.nix -A tarball $(NIX_ARGS)

test:
	nix-build release.nix -A build.$(SYSTEM).$(PYTHON)
	nix-shell --run "bin/code-analysis" $(NIX_ARGS)

coverage: .coverage
	nix-shell --run "coverage report --fail-under=80"

.PHONY: all env docs dist test

###

.coverage: $(TEST) $(SRC)
	nix-shell --run "coverage run setup.py test"

result/bin/$(PYTHON):
	nix-build release.nix -A buildEnv.$(SYSTEM).$(PYTHON)

result/sphinxcontrib-httpexample.pdf:
	nix-build release.nix -A docs
