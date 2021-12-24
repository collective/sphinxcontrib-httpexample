{ nixpkgs ? sources."nixpkgs-21.11"
, config ? {
  permittedInsecurePackages = [
    "python2.7-pillow-6.2.2"
  ];
}
, sources ? import ./sources.nix
}:

let

  overlay = _: pkgs: {
    inherit (import sources."gitignore.nix" { inherit (pkgs) lib; }) gitignoreSource;
    inherit (import (sources."pip2nix" + "/release.nix") {
      # pip2nix branches require specific nixpkgs branch (for pip)
      pkgs = import sources."nixpkgs-20.09" {};
    }) pip2nix;
  };

  pkgs = import nixpkgs {
    overlays = [ overlay ];
    inherit config;
  };

in pkgs
