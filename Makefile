all: test

env: result/bin/python
	nix-build release.nix -A python

docs: result/sphinxcontrib-httpexample.pdf
	nix-build release.nix -A docs

dist:
	nix-build release.nix -A tarball

test:
	nix-shell --run "bin/code-analysis"
	nix-build release.nix -A docs

.PHONY: all env docs dist test

###

result/bin/python:
	nix-build release.nix -A python

result/sphinxcontrib-httpexample.pdf:
	nix-build release.nix -A docs
