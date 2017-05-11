{ supportedSystems ? [ "x86_64-linux" "x86_64-darwin" ]
, supportedPythons ? [ "python2" "python3" ]
, rev ? "28dc5c7d221ac0e13b8f5761459829fdf43a223c"  # 16.09
, sha256 ? "1yshwmbn7dk7hl9f3i8miz4928s1bvazmcxmm5x6q3q8q4y8i039"
, pkgs ? import ((import <nixpkgs> {}).pkgs.fetchFromGitHub {
    owner = "NixOS";
    repo = "nixpkgs";
    inherit rev;
    inherit sha256;
  }) {}
}:

let

  pkgFor = system: python:
    let syspkgs = import pkgs.path { inherit system; };
    in import ./default.nix {
      pkgs = syspkgs;
      pythonPackages = builtins.getAttr (python + "Packages") syspkgs;
    };

in rec {

  inherit pkgs;

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
