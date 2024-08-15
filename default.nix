{ system ? builtins.currentSystem
, pkgs ? import ../../nix { nixpkgs = sources."nixpkgs-20.09"; inherit system; }
, sources ? import ../../nix/sources.nix
, setup ? import ./setup.nix { inherit pkgs; }
}:

setup.build
