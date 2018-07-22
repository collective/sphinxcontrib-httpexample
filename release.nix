{ pkgs ? import (builtins.fetchTarball {
    # update sha256 with value of "nix-prefetch-url --unpack [url]"
    url = "https://github.com/NixOS/nixpkgs-channels/archive/d6c6c7fcec6dbd2b8ab14f0b35d56c7733872baa.tar.gz";
    sha256 = "1bq59575b58lmh5w8bh7pwp17c3p2nm651bz1i3q224c4zsj9294";  # nixos-18.03 at 2018-07-22
  }) {}
, supportedSystems ? [ "x86_64-linux" "x86_64-darwin" ]
, supportedPythons ? [ "python2" "python3" ]
, setup ? import ./setup.nix
}:

let

  pkgFor = system: python: setup { pkgs = import pkgs.path { inherit system; };
                                   python = python; };

in {

  build = pkgs.lib.genAttrs supportedSystems (system:
          pkgs.lib.genAttrs supportedPythons (python: pkgs.lib.hydraJob (
    (pkgFor system python).build)));

  sdist = pkgs.lib.hydraJob(
    (pkgFor builtins.currentSystem "python3").sdist);

  bdist_wheel = pkgs.lib.hydraJob(
    (pkgFor builtins.currentSystem "python3").bdist_wheel);

  docs =
    let pkg = pkgFor builtins.currentSystem "python2";
        env = pkgs.python2.withPackages
          (ps: [ pkg.build pkg.pythonPackages.rst2pdf ]);
    in pkgs.lib.hydraJob(pkg.build.overrideDerivation(old: {
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
