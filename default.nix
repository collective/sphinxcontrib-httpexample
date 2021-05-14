{ pkgs ? import ./nix { nixpkgs = sources."nixpkgs"; }
, sources ? import ./nix/sources.nix {}
, python ? "python39"
}:

(import ./setup.nix { inherit pkgs sources python; }).package
