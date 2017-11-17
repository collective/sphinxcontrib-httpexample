{ pkgs, pythonPackages }:

self: super: rec {

  setuptools = pythonPackages.setuptools;

  "flake8" = super."flake8".overrideDerivation (old: {
    buildInputs = old.buildInputs ++ [self."pytest-runner"];
  });

  "flake8-debugger" = super."flake8-debugger".overrideDerivation (old: {
    buildInputs = old.buildInputs ++ [self."pytest-runner"];
  });

  "mccabe" = super."mccabe".overrideDerivation (old: {
    buildInputs = old.buildInputs ++ [self."pytest-runner"];
  });

  "pillow" = pythonPackages."pillow".overrideDerivation(old:
    with super.pillow; {
      inherit name;
      inherit src;
      propagatedBuildInputs = [ self.olefile ];
    }
  );

  "pytest" = super."pytest".overrideDerivation (old: {
    buildInputs = old.buildInputs ++ [self."setuptools-scm"];
  });

  "pytest-runner" = super."pytest-runner".overrideDerivation (old: {
    buildInputs = old.buildInputs ++ [self."setuptools-scm"];
  });

  "reportlab" = pythonPackages."reportlab".overrideDerivation(old:
    with super.reportlab; {
      inherit name;
      inherit src;
    }
  );

  "rst2pdf" = super."rst2pdf".overrideDerivation(old: {
    propagatedBuildInputs = old.propagatedBuildInputs ++ [ pillow ];
  });

  "sphinx" = super."sphinx".overrideDerivation(old: {
    propagatedBuildInputs = old.propagatedBuildInputs ++ [ super.typing ];
  });

}
