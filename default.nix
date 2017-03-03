#!/usr/bin/env nix-shell
#! nix-shell --arg "pkgs" "import <nixpkgs> {}"
{ pkgs ? import (builtins.fetchTarball
  "https://github.com/nixos/nixpkgs-channels/archive/nixos-16.09.tar.gz") {}
, pythonPackages ? pkgs.python3Packages
}:

let self = rec {
  version = builtins.replaceStrings ["\n"] [""] (builtins.readFile ./VERSION);

  buildout = pythonPackages.zc_buildout_nix.overrideDerivation(old: {
    postInstall = "";
  });

  pdfrw = pythonPackages.buildPythonPackage {
    name = "pdfrw-0.3";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/06/62/7f43c4a9d014b94ea03fe73088332fa07db1a03f806bac01aaa19a7fb887/pdfrw-0.3.tar.gz";
      sha256 = "0dlg2hz5x7y3bhrj2d7bm792wyx7ghy3w867dj27vh6j07rqmw8s";
    };
    doCheck = false;  # tests excluded from source distribution
  };

  rst2pdf = pythonPackages.buildPythonPackage {
    name = "rst2pdf-0.93";
    src = pkgs.fetchurl {
      url = "https://github.com/rst2pdf/rst2pdf/archive/0.93.tar.gz";
      sha256 = "37e99ea103790321b29b6f6b0192821ba9c2990a6aec57295585ca6919932a97";
    };
    propagatedBuildInputs = [
      pdfrw
      pythonPackages.pillow
      pythonPackages.docutils
      pythonPackages.future
      pythonPackages.pygments
      pythonPackages.reportlab
    ];
    doCheck = false;  # tests excluded from source distribution
  };
};

in pythonPackages.buildPythonPackage rec {
  namePrefix = "";
  name = "sphinxcontrib-httpexample-${self.version}";
  src = builtins.filterSource
    (path: type: baseNameOf path != ".git"
              && baseNameOf path != "result")
    ./.;
  buildInputs = with self; [
    buildout
    rst2pdf
    pkgs.git
    pythonPackages.check-manifest
    pythonPackages.sphinx_rtd_theme
  ];
  propagatedBuildInputs = with self; [
    pythonPackages.sphinx
    pythonPackages.sphinxcontrib_httpdomain
  ];
  shellHook = ''
    buildout -Nc qa.cfg install code-analysis
  '';
}
