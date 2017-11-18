all: requirements.nix

requirements.nix: ../requirements.txt
	nix-shell pip2nix.nix \
	  --run "pip2nix generate -r ../requirements.txt --output=requirements.nix"
