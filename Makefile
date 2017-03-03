PYTHON ?= python3

all: test

python: result/bin/python3

docs: result/sphinxcontrib-httpexample.pdf

dist:
	nix-build release.nix -A tarball $(NIX_ARGS)

test:
	nix-shell --run "bin/code-analysis"  $(NIX_ARGS)
	nix-build release.nix -A build_$(PYTHON)

.PHONY: all env docs dist test

###

result/bin/python3:
	nix-build release.nix -A $(PYTHON)

result/sphinxcontrib-httpexample.pdf:
	nix-build release.nix -A docs
