{ pkgs, pythonPackages }:

self: super: {

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

}
