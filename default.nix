#!/usr/bin/env nix-shell
{ pkgs ? (import ./release.nix {}).pkgs
, python ? "python3"
, pythonPackages ? builtins.getAttr (python + "Packages") pkgs
}:

let dependencies = rec {

  buildout = pythonPackages.zc_buildout_nix.overrideDerivation(old: {
    postInstall = "";
  });

  astunparse = pythonPackages.buildPythonPackage {
    name = "astunparse-1.5.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/1a/b7/3ba7ce33cbc8847e20ed1a4fbec2303a71b2512dec0194824e8dcaadc8de/astunparse-1.5.0.tar.gz";
      sha256 = "55df3c2a659d6cb6a9a9041c750a8232a9925523405a8dfeb891b92d45a589cd";
    };
    propagatedBuildInputs = [
      pythonPackages.six
    ];
    doCheck = false;  # tests excluded from source distribution
  };

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

  coveralls = pythonPackages.buildPythonPackage {
    name = "coveralls-1.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/12/50/5c1034eb92e5bc3d824a3745ca9162f2e4846c6ab5f96dccb5f84f77e98f/coveralls-1.1.tar.gz";
      sha256 = "34160385c13b0c43691ab11c080d4b10dabe3280fc0b2173c731efc5db836808";
    };
    propagatedBuildInputs = [
      pythonPackages.docopt
      pythonPackages.coverage
      pythonPackages.requests2
      pythonPackages.pyyaml
    ];
    doCheck = false;
  };

  check-manifest = pythonPackages.buildPythonPackage rec {
    name = "check-manifest-0.30";

    src = pkgs.fetchurl {
      url = "mirror://pypi/c/check-manifest/check-manifest-0.30.tar.gz";
      sha256 = "b19fd0d8b9286532ba3dc0282484fd76d11200cf24b340dc3d08f293c7dd0500";
    };

    doCheck = false;
  };
};

in pythonPackages.buildPythonPackage rec {
  version = builtins.replaceStrings ["\n"] [""] (builtins.readFile ./VERSION);
  name = "sphinxcontrib-httpexample-${version}";
  src = builtins.filterSource
    (path: type: baseNameOf path != ".git"
              && baseNameOf path != "result")
    ./.;
  SSL_CERT_FILE = "${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt";
  buildInputs = with dependencies; [
    buildout
    rst2pdf
    check-manifest
    coveralls
    pythonPackages.pytest
    pythonPackages.pytestrunner
    pythonPackages.coverage
    pythonPackages.sphinx_rtd_theme
    pythonPackages.sphinx-testing
  ];
  propagatedBuildInputs = with dependencies; [
    astunparse
    pythonPackages.sphinx
    pythonPackages.sphinxcontrib_httpdomain
  ];
  postShellHook = ''
    export SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt
    buildout -Nc qa.cfg
  '';
}
