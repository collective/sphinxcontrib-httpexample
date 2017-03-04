#!/usr/bin/env nix-build
#! nix-build --arg "pkgs" "import <nixpkgs> {}" -A python
{ supportedSystems ? [ "x86_64-linux" ]
, supportedPythons ? [ "python2" "python3" ]
, pkgs ? import (builtins.fetchTarball
  "https://github.com/nixos/nixpkgs-channels/archive/nixos-16.09.tar.gz") {}
}:

let

  pkgFor = system: python:
    let syspkgs = import pkgs.path { inherit system; };
    in import ./default.nix {
      pkgs = syspkgs;
      pythonPackages = builtins.getAttr (python + "Packages") syspkgs;
    };

in rec {

  build = pkgs.lib.genAttrs supportedSystems (system:
          pkgs.lib.genAttrs supportedPythons (python: pkgs.lib.hydraJob (
    pkgFor system python
  )));

  buildEnv = pkgs.lib.genAttrs supportedSystems (system:
             pkgs.lib.genAttrs supportedPythons (python: pkgs.lib.hydraJob (
    let package = pkgFor system python;
        syspkgs = import pkgs.path { inherit system; };
    in (builtins.getAttr python syspkgs).buildEnv.override {
      extraLibs = package.nativeBuildInputs
                  ++ package.propagatedNativeBuildInputs;
      ignoreCollisions = true;
    }
  )));

  tarball = pkgs.lib.hydraJob(
            (pkgFor "x86_64-linux" "python3").overrideDerivation(args: {
    phases = [ "unpackPhase" "buildPhase" ];
    buildPhase = ''
      ${buildEnv."x86_64-linux".python3}/bin/python3 setup.py sdist --formats=gztar
      mkdir -p $out/dist $out/nix-support
      mv dist/${args.name}.tar.gz $out/dist
      echo "file source-dist $out/dist/${args.name}.tar.gz" > \
           $out/nix-support/hydra-build-products
      echo ${args.name} > $out/nix-support/hydra-release-name
    '';
  }));

  # docs can only be built on Python 2, because of rst2pdf

  docs = pkgs.lib.hydraJob(
         (pkgFor "x86_64-linux" "python2").overrideDerivation(args: {
    phases = [ "unpackPhase" "buildPhase" ];
    buildPhase = ''
      ${docs_python}/bin/sphinx-build -b pdf docs dist
      mkdir -p $out/docs $out/nix-support
      mv dist/*.pdf $out/docs
      echo "file source-dist" $out/docs/*.pdf > \
           $out/nix-support/hydra-build-products
      echo ${args.name} > $out/nix-support/hydra-release-name
    '';
  }));

  docs_python = pkgs.lib.hydraJob (
    let system = "x86_64-linux";
        syspkgs = import pkgs.path { inherit system; };
    in syspkgs.python2.buildEnv.override {
      extraLibs = [ (pkgFor system "python2") ];
      ignoreCollisions = true;
    }
  );

}
