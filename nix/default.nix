{ nixpkgs ? sources.nixpkgs
, config ? {
  permittedInsecurePackages = [
    "python2.7-pillow-6.2.2"
  ];
}
, sources ? import ./sources.nix
}:

let

  overlay = _: pkgs: {
    # pip2nix branches require specific nixpkgs branch (for pip)
    pip2nix = ((import (sources."pip2nix" + "/release.nix") {
      pkgs = import sources."nixpkgs-20.09" {};
    }).pip2nix);
  };

  pkgs = import nixpkgs {
    overlays = [ overlay ];
    inherit config;
  };

in pkgs
