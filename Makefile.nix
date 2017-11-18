PYTHON ?= python3
ARGSTR ?= --arg pkgs "import <nixpkgs> {}" --argstr python $(PYTHON)

%: nix-support/requirements.nix
	nix-shell nix-support $(ARGSTR) -A shell \
	  --run 'nix-shell $(ARGSTR) --run "$(MAKE) $@"'

env: nix-support/requirements.nix
	nix-build nix-support $(ARGSTR) -A env

docs: nix-support/requirements.nix
	nix-build release.nix $(ARGSTR) -A docs

shel: nix-support/requirements.nix
	nix-shell $(ARGSTR)

.PHONY: env

nix-support/requirements.nix: requirements.txt
	make -C nix-support
