{ pkgs ? import <nixpkgs> {}
, supportedSystems ? [ "x86_64-linux" "x86_64-darwin" ]
, supportedPythons ? [ "python2" "python3" ]
}:

let

  pkgFor = system: python:
    let syspkgs = import pkgs.path { inherit system; };
        support = import ./nix-support { pkgs = syspkgs; inherit python; };
    in import ./default.nix {
      pkgs = syspkgs;
      inherit (support) pythonPackages;
    };

  envFor = system: python: packages:
    let syspkgs = import pkgs.path { inherit system; };
        support = import ./nix-support { pkgs = syspkgs; inherit python; };
    in support.pythonPackages.python.withPackages (ps: [
      (pkgFor system python)
    ] ++ builtins.map
      (name: builtins.getAttr name support.pythonPackages) packages
    );

in {

  build = pkgs.lib.genAttrs supportedSystems (system:
          pkgs.lib.genAttrs supportedPythons (python: pkgs.lib.hydraJob (
    pkgFor system python
  )));

  sdist =
    let package = pkgFor builtins.currentSystem "python3";
        env = envFor builtins.currentSystem "python3" [];
    in pkgs.lib.hydraJob(package.overrideDerivation(old: {
      name = "${old.name}-sdist";
      phases = [ "unpackPhase" "buildPhase" ];
      buildPhase = ''
        ${env}/bin/python setup.py sdist --formats=gztar
        mkdir -p $out/dist $out/nix-support
        mv dist/*.tar.gz $out/dist
        for file in `ls -1 $out/dist`; do
          echo "file source-dist $out/dist/$file" >> \
               $out/nix-support/hydra-build-products
        done
        echo ${old.name} > $out/nix-support/hydra-release-name
      '';
    }));

  bdist_wheel =
    let package = pkgFor builtins.currentSystem "python3";
        env = envFor builtins.currentSystem "python3" [];
    in pkgs.lib.hydraJob(package.overrideDerivation(old: {
      name = "${old.name}-bdist_wheel";
      phases = [ "unpackPhase" "buildPhase" ];
      buildPhase = ''
        ${env}/bin/python setup.py bdist_wheel
        mkdir -p $out/dist $out/nix-support
        mv dist/*.whl $out/dist
        for file in `ls -1 $out/dist`; do
          echo "file binary-dist $out/dist/$file" >> \
               $out/nix-support/hydra-build-products
        done
        echo ${old.name} > $out/nix-support/hydra-release-name
      '';
    }));

  # docs can only be built on Python 2, because of rst2pdf

  docs =
    let package = pkgFor builtins.currentSystem "python2";
        env = envFor builtins.currentSystem "python2" ["rst2pdf"];
    in pkgs.lib.hydraJob(package.overrideDerivation(old: {
      name = "${old.name}-docs";
      phases = [ "unpackPhase" "buildPhase" ];
      buildPhase = ''
        mkdir -p $out/docs $out/nix-support
        ${env}/bin/sphinx-build -b html docs $out/docs/html
        ${env}/bin/sphinx-build -b pdf  docs $out/docs
        echo "file source-dist" $out/docs/*.pdf > \
             $out/nix-support/hydra-build-products
        echo ${old.name} > $out/nix-support/hydra-release-name
      '';
    }));

}
