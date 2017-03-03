#!/usr/bin/env nix-build
#! nix-build --arg "pkgs" "import <nixpkgs> {}" -A python
{ supportedSystems ? [ "x86_64-linux" ]
, pkgs ? import (builtins.fetchTarball
  "https://github.com/nixos/nixpkgs-channels/archive/nixos-16.09.tar.gz") {}
}:

let

  pkgFor = system: pythonPackages: import ./default.nix {
    pkgs = import pkgs.path { inherit system; };
    inherit pythonPackages;
  };

in rec {

  build = build_python3;

  build_python2 = pkgs.lib.genAttrs supportedSystems (system: pkgs.lib.hydraJob (
    pkgFor system pkgs.python2Packages
  ));

  build_python3 = pkgs.lib.genAttrs supportedSystems (system: pkgs.lib.hydraJob (
    pkgFor system pkgs.python3Packages
  ));

  python = python3;

  python3 = pkgs.lib.genAttrs supportedSystems (system: pkgs.lib.hydraJob (
    let package = pkgFor system pkgs.python3Packages;
        syspkgs = import pkgs.path { inherit system; };
    in syspkgs.python3.buildEnv.override {
      extraLibs = package.nativeBuildInputs
                  ++ package.propagatedNativeBuildInputs;
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

  docs = pkgs.lib.hydraJob((pkgFor "x86_64-linux" pkgs.python2Packages)
                 .overrideDerivation(args: {
    phases = [ "unpackPhase" "buildPhase" ];
    buildPhase = ''
      ${docs_python}/bin/sphinx-build -b pdf docs dist
      mkdir -p $out/nix-support
      mv dist/*.pdf $out
      echo "file source-dist" $out/*.pdf > \
           $out/nix-support/hydra-build-products
      echo ${args.name} > $out/nix-support/hydra-release-name
    '';
  }));

  docs_python = pkgs.lib.hydraJob (
    let system = "x86_64-linux";
        package = pkgFor system pkgs.python2Packages;
        syspkgs = import pkgs.path { inherit system; };
    in syspkgs.python2.buildEnv.override {
      extraLibs = [ package ];
      ignoreCollisions = true;
    }
  );

}
