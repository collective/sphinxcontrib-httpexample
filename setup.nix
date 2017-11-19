{ pkgs ? import <nixpkgs> {}
, python ? "python3"
, pythonPackages ? builtins.getAttr (python + "Packages") pkgs
, setup ? import (pkgs.fetchFromGitHub {
    owner = "datakurre";
    repo = "setup.nix";
    rev = "6654411b3a1438b8a38dcf29237e857d652bd5a1";
    sha256 = "0dqsbffsddj01rw3cddg5warxfkplkpprhki1d7rw8m6mhcm02qw";
  })
}:

let overrides = self: super: {

  flake8 = super.flake8.overrideDerivation (old: {
    buildInputs = old.buildInputs ++ [ self.pytest-runner ];
    propagatedBuildInputs = old.propagatedBuildInputs ++ [ self.enum34 self.configparser ];
  });

  flake8-debugger = super.flake8-debugger.overrideDerivation (old: {
    buildInputs = old.buildInputs ++ [ self.pytest-runner ];
  });

  mccabe = super.mccabe.overrideDerivation (old: {
    buildInputs = old.buildInputs ++ [ self.pytest-runner ];
  });

  olefile = pythonPackages.olefile;

  pillow = pythonPackages.pillow.overrideDerivation(old:
    with super.pillow; { inherit name src; }
  );

  pytest = super.pytest.overrideDerivation (old: {
    buildInputs = old.buildInputs ++ [ self.setuptools-scm ];
  });

  pytest-runner = super.pytest-runner.overrideDerivation (old: {
    buildInputs = old.buildInputs ++ [ self.setuptools-scm ];
  });

  reportlab = pythonPackages.reportlab.overrideDerivation(old:
    with super.reportlab; { inherit name src; }
  );

  rst2pdf = super.rst2pdf.overrideDerivation(old: {
    propagatedBuildInputs = old.propagatedBuildInputs ++ [ self.pillow ];
  });

  setuptools = pythonPackages.setuptools;

  sphinx = super.sphinx.overrideDerivation(old: {
    propagatedBuildInputs = old.propagatedBuildInputs ++ [ self.typing self.configparser];
  });

};

in setup {
  inherit pkgs pythonPackages overrides;
  src = ./.;
}
