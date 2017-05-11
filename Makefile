SYSTEM ?= x86_64-linux
PYTHON ?= python3

TEST = $(wildcard tests/*.py)
SRC = $(wildcard src/sphinxcontrib/httpexample/*.py)

all: test

buildEnv: result/bin/$(PYTHON)

coverage: .coverage
	nix-shell --run "coverage report --fail-under=80" \
	          --argstr "python" $(PYTHON)

coveralls: .coverage
	nix-shell --run coveralls \
	          --argstr "python" $(PYTHON)

dist:
	nix-build release.nix -A tarball

docs: result/sphinxcontrib-httpexample.pdf

shell:
	nix-shell --argstr "python" $(PYTHON)

test:
	nix-build release.nix -A build.$(SYSTEM).$(PYTHON)
	nix-shell --run "bin/code-analysis" \
	          --argstr "python" $(PYTHON)

.PHONY: all buildEnv coverage coveralls dist docs shell test

###

.coverage: $(TEST) $(SRC)
	nix-shell --run "coverage run setup.py test" \
	          --argstr "python" $(PYTHON)

result/bin/$(PYTHON):
	nix-build release.nix -A buildEnv.$(SYSTEM).$(PYTHON)

result/sphinxcontrib-httpexample.pdf:
	nix-build release.nix -A docs
