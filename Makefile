all: test

python: result/bin/python
	nix-build release.nix -A python

docs: result/sphinxcontrib-httpexample.pdf
	nix-build release.nix -A python

test:
	nix-build release.nix -A docs

###

result/bin/python:
	nix-build release.nix -A python

result/sphinxcontrib-httpexample.pdf:
	nix-build release.nix -A docs
