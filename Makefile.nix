PYTHON ?= python3
ARGSTR ?= --argstr python $(PYTHON)

%: nix-support/requirements.nix
	nix-shell nix-support $(ARGSTR) -A shell \
	  --run 'nix-shell $(ARGSTR) --run "$(MAKE) $@"'

docs: nix-support/requirements.nix
	nix-build release.nix $(ARGSTR) -A docs

env: nix-support/requirements.nix
	nix-build nix-support $(ARGSTR) -A env

shell: nix-support/requirements.nix
	nix-shell $(ARGSTR)

.PHONY: docs env shell

nix-support/requirements.nix:
	make -C nix-support
