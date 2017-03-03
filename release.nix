#!/usr/bin/env nix-build
#! nix-build --arg "pkgs" "import <nixpkgs> {}" -A python
{ supportedSystems ? [ "x86_64-linux" ]
, pkgs ? import (builtins.fetchTarball
  "https://github.com/nixos/nixpkgs-channels/archive/nixos-16.09.tar.gz") {}
}:

let

  pkgFor = system: import ./default.nix {
    pkgs = import pkgs.path { inherit system; };
  };

in rec {

  build = pkgs.lib.genAttrs supportedSystems (system: pkgs.lib.hydraJob (
    pkgFor system
  ));

  python = pkgs.lib.genAttrs supportedSystems (system: pkgs.lib.hydraJob (
    let package = pkgFor system;
        syspkgs = import pkgs.path { inherit system; };
    in syspkgs.python2.buildEnv.override {
      extraLibs = package.nativeBuildInputs
                  ++ package.propagatedNativeBuildInputs;
      ignoreCollisions = true;
    }
  ));

  env = pkgs.lib.genAttrs supportedSystems (system: pkgs.lib.hydraJob (
    let package = pkgFor system;
        syspkgs = import pkgs.path { inherit system; };
    in syspkgs.python2.buildEnv.override {
      extraLibs = [ package ];
      ignoreCollisions = true;
    }
  ));

  tarball = pkgs.lib.hydraJob((pkgFor "x86_64-linux")
                    .overrideDerivation(args: {
    phases = [ "unpackPhase" "buildPhase" ];
    buildPhase = ''
      ${python."x86_64-linux"}/bin/python2 setup.py sdist --formats=gztar
      mkdir -p $out/tarballs $out/nix-support
      mv dist/${args.name}.tar.gz $out/tarballs
      echo "file source-dist $out/tarballs/${args.name}.tar.gz" > \
           $out/nix-support/hydra-build-products
      echo ${args.name} > $out/nix-support/hydra-release-name
    '';
  }));

  docs = pkgs.lib.hydraJob((pkgFor "x86_64-linux")
                 .overrideDerivation(args: {
    phases = [ "unpackPhase" "buildPhase" ];
    buildPhase = ''
      ${env."x86_64-linux"}/bin/sphinx-build -b pdf docs dist
      mkdir -p $out/nix-support
      mv dist/*.pdf $out
      echo "file source-dist" $out/*.pdf > \
           $out/nix-support/hydra-build-products
      echo ${args.name} > $out/nix-support/hydra-release-name
    '';
  }));
}
