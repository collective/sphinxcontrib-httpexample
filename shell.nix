{ pkgs ? import ./nix { nixpkgs = sources."nixpkgs"; }
, sources ? import ./nix/sources.nix {}
, python ? "python39"
}:

with pkgs;

mkShell {
  buildInputs = [
    (lib.getAttr python pkgs.pip2nix)
  ];
}
