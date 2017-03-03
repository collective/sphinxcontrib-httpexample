SYSTEM ?= x86_64-linux
PYTHON ?= python3

TEST = $(wildcard tests/*.py)
SRC = $(wildcard src/sphinxcontrib/httpexample/*.py)

all: test

python: result/bin/$(PYTHON)

docs: result/sphinxcontrib-httpexample.pdf

dist:
	nix-build release.nix -A tarball $(NIX_ARGS)

test:
	nix-shell --run "bin/code-analysis" $(NIX_ARGS)
	nix-build release.nix -A build.$(SYSTEM).$(PYTHON)

coverage: .coverage
	nix-shell --run "coverage report --fail-under=80"

.PHONY: all env docs dist test

###

.coverage: $(TEST) $(SRC)
	nix-shell --run "coverage run setup.py test"

result/bin/$(PYTHON):
	nix-build release.nix -A env.$(SYSTEM).$(PYTHON)

result/sphinxcontrib-httpexample.pdf:
	nix-build release.nix -A docs
